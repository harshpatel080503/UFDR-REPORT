import numpy as np
from sklearn.metrics import mean_absolute_error, accuracy_score
from rouge_score import rouge_scorer
import json

def calculate_rouge(generated, reference):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)
    return {
        "rouge1": scores['rouge1'].fmeasure,
        "rouge2": scores['rouge2'].fmeasure,
        "rougeL": scores['rougeL'].fmeasure
    }

def calculate_faithfulness(reasoner, generated_summary, evidence):
    """
    Uses the Reasoner (LLM) as a judge to determine if the summary is faithful to the evidence.
    Returns a score from 0.0 to 1.0.
    """
    if not evidence or not generated_summary:
        return 0.0
        
    evidence_text = ""
    for i, rec in enumerate(evidence, 1):
        evidence_text += f"\n[{i}] {rec.get('date', '')} | {rec.get('user', '')} | {rec.get('text', '')}"

    prompt = (
        "You are an impartial judge evaluating the faithfulness of a generated summary to the provided evidence.\n"
        "Given the EVIDENCE below, and the GENERATED SUMMARY, determine if all claims in the summary are fully supported by the evidence.\n\n"
        f"EVIDENCE:\n{evidence_text}\n\n"
        f"GENERATED SUMMARY:\n{generated_summary}\n\n"
        "Output ONLY a valid JSON object with a single field 'faithfulness_score' containing a float between 0.0 (completely hallucinated) and 1.0 (fully supported)."
    )
    
    # We use the internal narrative caller for a raw prompt
    # Note: Depending on Reasoner implementation, we might need to parse this carefully
    try:
        res = reasoner._call_llm_narrative("You are a metric evaluator.", prompt, timeout=120)
        
        # 1. Clean markdown blocks
        if "```json" in res:
            res = res.split("```json")[-1].split("```")[0].strip()
        elif "```" in res:
            res = res.split("```")[-1].split("```")[0].strip()
            
        # 2. Try standard JSON parsing
        try:
            start_idx = res.find("{")
            end_idx = res.rfind("}")
            if start_idx != -1 and end_idx != -1:
                data = json.loads(res[start_idx:end_idx+1])
                return float(data.get("faithfulness_score", 0.0))
            else:
                data = json.loads(res)
                return float(data.get("faithfulness_score", 0.0))
        except Exception:
            # 3. Regex Fallback for "faithfulness_score": 0.X
            import re
            match = re.search(r'"faithfulness_score":\s*([0-9\.]+)', res)
            if match:
                return float(match.group(1))
            
            # 4. Final Fallback for just a float in the response
            match_float = re.search(r'([0-1]\.[0-9]+)', res)
            if match_float:
                return float(match_float.group(1))
                
            raise
            
    except Exception as e:
        print(f"    [!] Faithfulness Evaluation Error: {e}")
        return 0.0

def evaluate_generator(reasoner, dataset, retriever=None):
    """
    Evaluate the Generator on Task metrics (Accuracy, MAE) and Grounding (ROUGE, Faithfulness).
    """
    print(f"\n[+] Evaluating Generator (Task & Grounding Metrics)...")
    
    y_true_threat = []
    y_pred_threat = []
    
    y_true_risk = []
    y_pred_risk = []
    
    rouge_scores = {"rouge1": [], "rouge2": [], "rougeL": []}
    faithfulness_scores = []
    
    for item in dataset:
        query = item["query"]
        expected_threat = item.get("expected_threat_category", "")
        expected_risk = item.get("expected_risk_score", 0)
        ideal_summary = item.get("ideal_summary", "")
        
        # If we have a retriever, get real evidence, otherwise mock it for isolated generator testing
        if retriever:
            results, _, _ = retriever.search(query, k=10, use_reranker=True)
            evidence = results
        else:
            evidence = [{"date": "2010", "user": "test", "text": "mock evidence for generator test", "action": "test"}]
            
        # Run Reasoning Engine
        analysis = reasoner.analyze(query, evidence)
        
        pred_threat = analysis.get("threat_category", "")
        pred_risk = analysis.get("risk_score", 0)
        pred_summary = analysis.get("summary", "")
        
        # 1. Threat Category Accuracy
        if expected_threat:
            y_true_threat.append(str(expected_threat).strip().lower())
            y_pred_threat.append(str(pred_threat).strip().lower())
            
        # 2. Risk Score Error
        y_true_risk.append(expected_risk)
        y_pred_risk.append(pred_risk)
        
        # 3. ROUGE (Text Quality)
        if ideal_summary and pred_summary:
            r_scores = calculate_rouge(pred_summary, ideal_summary)
            rouge_scores["rouge1"].append(r_scores["rouge1"])
            rouge_scores["rouge2"].append(r_scores["rouge2"])
            rouge_scores["rougeL"].append(r_scores["rougeL"])
            
        # 4. Faithfulness (Grounding)
        if pred_summary and evidence:
            faith_score = calculate_faithfulness(reasoner, pred_summary, evidence)
            faithfulness_scores.append(faith_score)
            
    # Aggregate
    agg_metrics = {}
    
    if y_true_threat:
        agg_metrics["threat_accuracy"] = accuracy_score(y_true_threat, y_pred_threat)
    
    if y_true_risk:
        agg_metrics["risk_score_mae"] = mean_absolute_error(y_true_risk, y_pred_risk)
        
    for k, v in rouge_scores.items():
        if v:
            agg_metrics[k] = np.mean(v)
            
    if faithfulness_scores:
        agg_metrics["faithfulness"] = np.mean(faithfulness_scores)
        
    return agg_metrics

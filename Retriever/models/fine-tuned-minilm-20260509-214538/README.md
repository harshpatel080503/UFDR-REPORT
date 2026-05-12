---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:732
- loss:MultipleNegativesRankingLoss
base_model: sentence-transformers/all-MiniLM-L6-v2
widget:
- source_sentence: What users visited secureserver.net on 2010-03-23 and why does
    the URL look like it's encoded
  sentences:
  - OMS0101 visited http://inbox.com/Cheadle_Hulme/hulme/yrnqrefuvcnanylfvfselvat513824541.aspx
    content southern 200 advantage fall personally 1966 detailed named injured hampered
    experienced channel owne
  - CHG0146 visited http://secureserver.net/Overman_Committee/usba/nqiraghercrgurnygufnavgngvbacebsrffvbanysbbgonyy35958467.jsp
    content american cuban certain steamship american simpson begun losses identified
    high these just from stree
  - DTP0379 visited http://digitalpoint.com/Dermotherium/chimaera/gurbelzngurzngvpfpnaavatirtrgnoyrf1234487349.jsp
    content overruled wounded shells failed gas name uprising two peaceful was authorise
    law encouraging interna
- source_sentence: query 2
  sentences:
  - NSS0876 Logoff on PC-5910
  - IWM0816 visited http://eonline.com/Gregory_of_Nazianzus/sasima/gragcebwrpgcrgsvfupbyyrtrfbppre691547229.htm
    content donald who cast letter leader thousand entered tariffs people terms last
    wish april sector legislati
  - 'VSS0154 visited http://1saleaday.com/Mercury_dime/dimes/frphevglsvernhgbercnveznahnyf1114821738.aspx
    content reached insanity robbed mute acquittals leg along multi struggle on put
    leaving now ten controversy '
- source_sentence: Identify potential data exfiltration activity involving users accessing
    1saleaday.com
  sentences:
  - MAH0864 visited http://1saleaday.com/Mercury_dime/dimes/frphevglsvernhgbercnveznahnyf1114821738.aspx
    content below sued working formed jamaica just july steadily professor human deputy
    fled criticized chancell
  - AMH0794 visited http://nymag.com/Terra_Nova_Expedition/koettlitz/qbjaevttvatpnzcpbbxvatzngurzngvpf2145772149.htm
    content disagreed before sacrifices purposes colonial 24 who in communists settled
    united renamed march illi
  - 'MOH0273 accessed 6IBWA48I.pdf content 25-50-44-46-2D raiding between 15th important
    enough ascending frequented president raised van separated source lindsay unnatural
    difficult adjoining '
- source_sentence: Identify suspicious activity involving FBA0348 involving downloading
    content from external URLs
  sentences:
  - AHC0142 visited http://inbox.com/Cheadle_Hulme/hulme/yrnqrefuvcnanylfvfselvat513824541.aspx
    content business heavily successfully designated link eight major indies naval
    overall encountered john nort
  - AHD0848 visited http://bizrate.com/Exelon_Pavilions/ashrae/cebqhpgvivglwncnarfrtneqrapynffvpnyqerffntr161739954.jsp
    content better displays fireplace fitting words doulting giles accepted overlooking
    1995 fitting roll privat
  - 'FBA0348 visited http://outbrain.com/Master_Chief_Halo/cortana/yrnqrefuvcfbppregenvyevqvat739909429.jsp
    content split change properly lakeshore revenge overall failing massively is papers
    lightly control headway '
- source_sentence: Find all log entries for FHO0630 from 2010-02-26 with content mentioning
    'harass' or 'malicious'
  sentences:
  - CKB0427 visited http://nfl.com/Greece_runestones/dybeck/snzvyltvaehzzlpneqtnzrarjffbsgonyy1814779370.jsp
    content 101 managing protect long security wound contain brown 148 difficult began
    overlooked ball slips don
  - JCR0921 emailed Xander-Doyle@juno.com;BMG8237@yahoo.com content photosynthesis
    unable unable saw sudden pieces shape nuclear from suggesting used 5 over gulf
    thousands atmosphere s 60 1970s surplus soon meanwhile available la indicated
    s these 2008 about meanwhile
  - FHO0630 visited http://clickbank.net/Blyth_Northumberland/blyth/ovyyvneqfobbxfculfvpfubefronpxevqvatfghagf117333686.jsp
    content harass so also upper human strict allowed culminating harass pull diverse
    likely lost by it gap resu
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on sentence-transformers/all-MiniLM-L6-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). It maps sentences & paragraphs to a 384-dimensional dense vector space and can be used for retrieval.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) <!-- at revision c9745ed1d9f207416be6d2e6f8de32d1f16199bf -->
- **Maximum Sequence Length:** 256 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
- **Supported Modality:** Text
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'BertModel'})
  (1): Pooling({'embedding_dimension': 384, 'pooling_mode': 'mean', 'include_prompt': True})
  (2): Normalize({})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```
Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    "Find all log entries for FHO0630 from 2010-02-26 with content mentioning 'harass' or 'malicious'",
    'FHO0630 visited http://clickbank.net/Blyth_Northumberland/blyth/ovyyvneqfobbxfculfvpfubefronpxevqvatfghagf117333686.jsp content harass so also upper human strict allowed culminating harass pull diverse likely lost by it gap resu',
    'CKB0427 visited http://nfl.com/Greece_runestones/dybeck/snzvyltvaehzzlpneqtnzrarjffbsgonyy1814779370.jsp content 101 managing protect long security wound contain brown 148 difficult began overlooked ball slips don',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[ 1.0000,  0.6267, -0.0021],
#         [ 0.6267,  1.0000,  0.2489],
#         [-0.0021,  0.2489,  1.0000]])
```
<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 732 training samples
* Columns: <code>sentence_0</code> and <code>sentence_1</code>
* Approximate statistics based on the first 732 samples:
  |         | sentence_0                                                                         | sentence_1                                                                        |
  |:--------|:-----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|
  | type    | string                                                                             | string                                                                            |
  | details | <ul><li>min: 2 tokens</li><li>mean: 21.56 tokens</li><li>max: 136 tokens</li></ul> | <ul><li>min: 13 tokens</li><li>mean: 66.5 tokens</li><li>max: 97 tokens</li></ul> |
* Samples:
  | sentence_0                                                                                                                                                                             | sentence_1                                                                                                                                                                                                                                        |
  |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>Find all log entries for FHO0630 from 2010-02-26 with content mentioning 'harass' or 'malicious'</code>                                                                          | <code>FHO0630 visited http://clickbank.net/Blyth_Northumberland/blyth/ovyyvneqfobbxfculfvpfubefronpxevqvatfghagf117333686.jsp content harass so also upper human strict allowed culminating harass pull diverse likely lost by it gap resu</code> |
  | <code>query 2</code>                                                                                                                                                                   | <code>DIB0285 visited http://nfl.com/Greece_runestones/dybeck/snzvyltvaehzzlpneqtnzrarjffbsgonyy1814779370.jsp content shots terminal weather education 5225 restrict remark attempting coach marked milestone songs armful</code>                |
  | <code>Find all log entries from JBM0350 on 02-22-2010 where the user action description contains 'hands' and any of the following words: 'entire', 'clipped', 'show', 'praised'</code> | <code>JBM0350 visited http://tigerdirect.com/European_Commission/barroso/gifrevrfzragbegernqzvyy220107153.html content both hands pleasure interview clipped themselves entire opportunity needed missed show praised beat </code>                |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 20.0,
      "similarity_fct": "cos_sim",
      "gather_across_devices": false,
      "directions": [
          "query_to_doc"
      ],
      "partition_mode": "joint",
      "hardness_mode": null,
      "hardness_strength": 0.0
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 3
- `max_steps`: -1
- `learning_rate`: 5e-05
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_steps`: 0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `optim_target_modules`: None
- `gradient_accumulation_steps`: 1
- `average_tokens_across_devices`: True
- `max_grad_norm`: 1
- `label_smoothing_factor`: 0.0
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `use_cache`: False
- `neftune_noise_alpha`: None
- `torch_empty_cache_steps`: None
- `auto_find_batch_size`: False
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `include_num_input_tokens_seen`: no
- `log_level`: passive
- `log_level_replica`: warning
- `disable_tqdm`: False
- `project`: huggingface
- `trackio_space_id`: None
- `trackio_bucket_id`: None
- `trackio_static_space_id`: None
- `per_device_eval_batch_size`: 16
- `prediction_loss_only`: True
- `eval_on_start`: False
- `eval_do_concat_batches`: True
- `eval_use_gather_object`: False
- `eval_accumulation_steps`: None
- `include_for_metrics`: []
- `batch_eval_metrics`: False
- `save_only_model`: False
- `save_on_each_node`: False
- `enable_jit_checkpoint`: False
- `push_to_hub`: False
- `hub_private_repo`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_always_push`: False
- `hub_revision`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `restore_callback_states_from_checkpoint`: False
- `full_determinism`: False
- `seed`: 42
- `data_seed`: None
- `use_cpu`: False
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `dataloader_prefetch_factor`: None
- `remove_unused_columns`: True
- `label_names`: None
- `train_sampling_strategy`: random
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `ddp_static_graph`: None
- `ddp_backend`: None
- `ddp_timeout`: 1800
- `fsdp`: []
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `deepspeed`: None
- `debug`: []
- `skip_memory_metrics`: True
- `do_predict`: False
- `resume_from_checkpoint`: None
- `warmup_ratio`: None
- `local_rank`: -1
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Time
- **Training**: 4.0 minutes

### Framework Versions
- Python: 3.12.0
- Sentence Transformers: 5.4.1
- Transformers: 5.8.0
- PyTorch: 2.11.0+cpu
- Accelerate: 1.13.0
- Datasets: 4.8.5
- Tokenizers: 0.22.2

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### MultipleNegativesRankingLoss
```bibtex
@misc{oord2019representationlearningcontrastivepredictive,
      title={Representation Learning with Contrastive Predictive Coding},
      author={Aaron van den Oord and Yazhe Li and Oriol Vinyals},
      year={2019},
      eprint={1807.03748},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/1807.03748},
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->
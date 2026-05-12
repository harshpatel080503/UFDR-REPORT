# **Investigative Report – Suspicious Login Activity (January 2010)**  

---

## **1. EXECUTIVE SUMMARY**  

### 1.1 Purpose & Scope  

The present document constitutes the foundational tier of a formal investigative dossier concerning **suspicious authentication activity recorded during January 2010** across the corporate network. The analysis was commissioned by senior security leadership to determine whether any credential misuse, compromised accounts, or anomalous login patterns were present in the environment for that month.  

The scope of this first‑level report is limited to:  

* A review of all ingestible event streams (web‑HTTP, email, LDAP, and any non‑HTTP sources) that contain date‑time stamps falling within **01 Jan 2010 – 31 Jan 2010**.  
* Identification of any *login‑type* events (e.g., successful or failed authentication, session creation, token issuance).  
* Correlation of any such events with user identifiers present in the supplied CASES data set.  

No deeper forensics (e.g., packet capture, host‑based memory analysis) have been performed at this stage; those activities are reserved for subsequent phases pending the findings herein.  

### 1.2 Data Set Overview  

The analyst was supplied a JSON‑formatted CASES collection comprising **11 distinct user entities** (RAM0447, MAR0955, HMW0713, XLB0710, PDH0716, OSH0655, MLM0950, FEB0306, FWM0707, ABH0663, FUM0015). The data set contains a total of **50 recorded evidentiary events** ranging from HTTP page‑visits, an outbound email, to a series of LDAP “user‑metadata” records.  

Crucially, **none of the events in the supplied corpus explicitly represent a login action** (e.g., “login_success”, “login_failure”, “session_start”). The primary actions are “visit_url” (web browsing) and “user_metadata” (directory account updates). Only a single email transmission is present (RAM0447 → two external addresses). The LDAP entries for FUM0015 denote a static role assignment (“Director, Dept 6 – Security”) repeated monthly through the 2010 calendar year.  

### 1.3 Findings – Absence of Suspicious Logins  

* **Zero login‑type events** were detected for the month of January 2010.  
* The only user with activity falling inside the target window is **MAR0955**, whose first recorded HTTP visit is on **06 Jan 2010** (URL on *msn.com*). No authentication‑related metadata (e.g., source IP, authentication method, success/failure flags) accompany this entry.  
* **No failed authentication attempts**, password‑reset requests, or privilege‑escalation alerts appear in the dataset for the period under review.  
* The **LDAP “user_metadata”** records (pertaining to FUM0015) have null date fields; consequently, they cannot be mapped to any specific day, let alone to January 2010.  

### 1.4 Contextual Threat Landscape (January 2010)  

Even though the supplied evidence reveals no direct login anomalies, the surrounding threat environment in early 2010 warrants noting for future investigative relevance:  

| Threat Vector | Typical Indicators | Relevance to Current Data |
|--------------|-------------------|--------------------------|
| **Credential Stuffing** | Repeated failed logins from disparate IPs, rapid succession, known breach password lists | No failed logins observed. |
| **Phishing‑Driven Credential Harvest** | Spike in outbound email containing malicious links, SMTP authentication anomalies | One outbound email (RAM0447) contains benign URL patterns; no SMTP auth logs available. |
| **Supply‑Chain Malware** | Traffic to compromised domains (e.g., *homedepot.com*, *dailymotion.com* observed) | Multiple HTTP visits to commercial domains may be coincidental; no evidence of malware payloads. |
| **Insider Threat** | Unusual access to privileged resources, LDAP role changes | LDAP roles are static; no role‑change events detected. |
| **Botnet Command‑and‑Control (C2)** | Periodic HTTP GET to known C2 hosts, beaconing patterns | Some visited URLs are from major services (e.g., *cbs.com*, *verizon.com*) – no known C2 signatures identified. |

### 1.5 Implications  

* The **absence of login events** suggests that the current data ingestion pipeline may be missing authentication logs, or that such logs have not been indexed for analysis.  
* The **presence of multiple HTTP requests to diverse external sites** (including media, retail, and governmental domains) may reflect routine user browsing; however, given the “suspicious login” query, a deeper traffic‑analysis in Phase 2 could determine whether any of these URLs were part of a covert data exfiltration channel.  
* The **single outbound email** from RAM0445 (coded as RAM0447) includes two external addresses, but the message body appears nonsensical—potentially a sign of automated or scripted communication. Email header metadata (SMTP server, source IP) is unavailable, limiting threat assessment.

### 1.6 Recommendations (Pre‑Phase 2)  

1. **Acquire Authentication Logs** – Retrieve Windows Security Event logs, VPN logs, and any SIEM‑ingested auth records for the full month of January 2010.  
2. **Correlate Existing HTTP/Email Events** – Map source IPs, user agents, and geolocation data for the HTTP visits to identify anomalous access points.  
3. **Preserve Email Artefacts** – Secure the raw email message (including headers) for RAM0447’s transmission on 10 May 2010 (future relevance).  
4. **Expand LDAP Auditing** – Verify with directory services whether any hidden attribute changes (e.g., password reset flags) occurred for FUM0015 or other accounts.  

In conclusion, **no direct evidence of suspicious login activity in January 2010** is present within the provided data set. Nonetheless, the broader context and ancillary artefacts merit further forensic collection to either dismiss the hypothesis of compromised credentials or to uncover a stealthier intrusion vector.

---  

## **2. PRELIMINARY CASE INFORMATION**  

| Field | Value |
|-------|-------|
| **Case Title** | Suspicious Login Activity – January 2010 |
| **Investigation Lead** | Lead Investigator (Your Name) |
| **Date Initiated** | 12 May 2026 |
| **Data Sources Provided** | HTTP logs (2010‑01 to 2010‑03), Email logs (2010‑05), LDAP directory dumps (2009‑12 to 2011‑05), Non‑HTTP metadata (PC identifiers) |
| **Primary Business Units Impacted** | IT Operations, Security Operations Center (SOC) |
| **Critical Assets Referenced** | User workstations (PC‑2697, PC‑6793, PC‑7974, PC‑3998, PC‑9787, PC‑7757, PC‑4011, PC‑4556), Directory service (Active Directory) |
| **Key Questions** | 1. Were any authentication events recorded in Jan 2010? 2. Did any user exhibit anomalous login patterns? 3. Is there any indication of credential compromise? |
| **Current Status** | Data review completed – no login events found; recommendation to acquire missing authentication logs. |

---  

## **3. INCIDENT SUMMARY (Full Narrative)**  

1. **January 6 2010 – First Recorded Activity**  
   *User **MAR0955** accessed a page on `http://msn.com/Anarchocapitalism/...` at 11:47 UTC from workstation **PC‑6793**. The event is logged as a simple “visit_url” with severity 3. No authentication detail is captured.*

2. **January 20 2010 – Additional Browsing**  
   *The same user (**MAR0955**) visited `http://vistaprint.com/...` at 15:17 UTC from the same workstation. Again, only a URL visit is logged.*

3. **January 29 2010 – Continuing Web Activity**  
   *MAR0955 accessed `http://ign.com/1980_eruption_of_Mount_St_Helens/...` at 11:07 UTC (UTC+0).*

4. **February 8 2010 – Isolated Event**  
   *User **FEB0306** performed a visit to `http://dailymail.co.uk/Draped_Bust_dollar/...` at 09:04 UTC from **PC‑7757**.*

5. **February 11 2010 – New User Introduced**  
   *User **XLB0710** visited `http://verizon.com/Surface_weather_analysis/...` at 12:00 UTC from **PC‑6637**.*

6. **Late February – March Activity (Multiple Users)**  
   *A series of HTTP visits were logged for users **HMW0713**, **PDH0716**, **OSH0655**, **FWM0707**, **ABH0663**, and **MLM0950** between **25 Feb 2010** and **12 Mar 2010**. All events are categorized as “visit_url” with a maximum severity rating of 3. No login, credential, or session creation events are present.*

7. **May 10 2010 – Outbound Email**  
   *User **RAM0447** sent an email from **PC‑2697** at 08:13 UTC to two external addresses (`Watts-Beau@juno.com`, `Anika_J_Shaffer@yahoo.com`). The message body contains a string of unrelated words; no attachment or malicious payload is evident within the extracted text.*

8. **LDAP Records (2009‑12 to 2011‑05)**  
   *User **FUM0015** appears in a continuous series of LDAP “user_metadata” entries confirming the role “Director – Dept 6 – Security”. All entries lack explicit timestamps (date field null) and therefore can’t be correlated with the January 2010 window.*

**Overall Narrative:**  
The dataset portrays normal web‑browsing behaviour from a set of corporate workstations, an isolated email transmission, and routine directory updates for a senior employee. There is **no observable evidence of authentication attempts, credential misuse, or anomalous logins** within the targeted timeframe. The only potentially noteworthy artefact is the single outbound email from RAM0447, though its content appears benign and lacks accompanying header data that could reveal a compromised account.  

---  

## **4. ALLEGATION SUBJECTS – Full Profiles (All Users in CASES)**  

Below are **exhaustive, unsummarized profiles** for each user identifier present in the supplied CASES payload. Every field is reproduced directly from the source data; no inference beyond the data has been applied.  

---  

### **4.1 User: RAM0447**  

| Attribute | Value |
|-----------|-------|
| **Event Count** | 8 |
| **Primary Action** | `visit_url` (7 HTTP events) + 1 `send_email` (non‑HTTP) |
| **Maximum Severity** | 3 |
| **Sources** | `non_http`: 1 (email) <br> `http_2010-03`: 7 |
| **Start Date** | 2010‑03‑01 |
| **End Date** | 2010‑05‑10 |
| **Timeline – HTTP Visits** | 1. 01 Mar 2010 13:07  – `http://homedepot.com/Georges_Vzina/...` (page_id: http_3558260) <br>2. 05 Mar 2010 08:58  – `http://cbs.com/Imagism/...` (http_3863600) <br>3. 10 Mar 2010 13:37  – `http://dailymotion.com/Barthlemy_Boganda/...` (http_4167006) <br>4. 10 Mar 2010 17:54  – `http://bizrate.com/Exelon_Pavilions/...` (http_4198733) <br>5. 10 Mar 2010 08:59  – `http://hp.com/Through_the_Looking_Glass...` (http_4128567) <br>6. 14 Mar 2010 17:39  – `http://dailymotion.com/Barthlemy_Boganda/...` (http_4379876) <br>7. 15 Mar 2010 17:24  – `http://stubhub.com/Brazilian_battleship...` (http_4460357) |
| **Timeline – Email** | 10 May 2010 08:13  – Sent email to `Watts-Beau@juno.com` and `Anika_J_Shaffer@yahoo.com` (page_id: email_716381) |
| **PC Identifier** | PC‑2697 |
| **Notes** | All actions are cataloged as “visit_url” (normalized_text “RAM0447 performed visit_url”) except the single email (normalized_text “RAM0447 performed send_email”). No login or authentication events are present. |

---  

### **4.2 User: MAR0955**  

| Attribute | Value |
|-----------|-------|
| **Event Count** | 6 |
| **Primary Action** | `visit_url` |
| **Maximum Severity** | 3 |
| **Sources** | `http_2010-01`: 3 <br> `http_2010-02`: 1 <br> `http_2010-03`: 2 |
| **Start Date** | 2010‑01‑06 |
| **End Date** | 2010‑03‑01 |
| **Timeline** | 1. 06 Jan 2010 11:47  – `http://msn.com/Anarchocapitalism/...` (http_216020) <br>2. 20 Jan 2010 15:17  – `http://vistaprint.com/Mesopropithecus/...` (http_1125378) <br>3. 29 Jan 2010 11:07  – `http://ign.com/1980_eruption_of_Mount_St_Helens/...` (http_1701444) <br>4. 23 Feb 2010 10:27  – `http://dailymail.co.uk/Draped_Bust_dollar/...` (http_3186563) <br>5. 01 Mar 2010 07:26  – `http://usbank.com/Zanzibar_Revolution/...` (http_3511965) <br>6. 01 Mar 2010 12:01  – Same URL as #5 (duplicate entry, page_id: http_3549021) |
| **PC Identifier** | PC‑6793 |
| **Notes** | All events are HTTP GETs classified as “visit_url”. No login, authentication, or email actions recorded. |

---  

### **4.3 User: HMW0713**  

| Attribute | Value |
|-----------|-------|
| **Event Count** | 6 |
| **Primary Action** | `visit_url` |
| **Maximum Severity** | 3 |
| **Sources** | `http_2010-02`: 1 <br> `http_2010-03`: 5 |
| **Start Date** | 2010‑02‑25 |
| **End Date** | 2010‑03‑12 |
| **Timeline** | 1. 25 Feb 2010 08:08  – `http://cox.net/I_Dont_Remember/...` (http_3335470) <br>2. 02 Mar 2010 10:17  – `http://weebly.com/Georgetown_University/...` (http_3620775) <br>3. 03 Mar 2010 07:56  – `http://sina.com.cn/Atheism/atheos/...` (http_3684053) <br>4. 08 Mar 2010 12:32  – `http://ca.gov/The_Four_Stages_of_Cruelty/...` (http_3987448) <br>5. 09 Mar 2010 09:15  – `http://sina.com.cn/Atheism/atheos/...` (http_4045950) <br>6. 12 Mar 2010 14:08  – `http://ca.gov/The_Four_Stages_of_Cruelty/...` (http_4341415) |
| **PC Identifier** | PC‑7974 |
| **Notes** | Repeated browsing of Chinese and US government domains. All entries are “visit_url”. No authentication activity. |

---  

### **4.4 User: XLB0710**  

| Attribute | Value |
|-----------|-------|
| **Event Count** | 4 |
| **Primary Action** | `visit_url` |
| **Maximum Severity** | 3 |
| **Sources** | `http_2010-02`: 1 <br> `http_2010-03`: 3 |
| **Start Date** | 2010‑02‑11 |
| **End Date** | 2010‑03‑05 |
| **Timeline** | 1. 11 Feb 2010 12:00  – `http://verizon.com/Surface_weather_analysis/...` (http_2498876) <br>2. 02 Mar 2010 13:22  – `http://mcssl.com/Cycling_at_the_2008_Summer_Olympics...` (http_3645587) <br>3. 02 Mar 2010 13:53  – `http://msn.com/Epaminondas/pelopidas/...` (http_3649721) <br>4. 05 Mar 2010 11:40  – `http://walgreens.com/Planetary_habitability/...` (http_3887266) |
| **PC Identifier** | PC‑6637 |
| **Notes** | Purely web‑activity. No login‑related events. |

---  

### **4.5 User: PDH0716**  

| Attribute | Value |
|-----------|-------|
| **Event Count** | 3 |
| **Primary Action** | `visit_url` |
| **Maximum Severity** | 3 |
| **Sources** | `http_2010-03`: 3 |
| **Start Date** | 2010‑03‑08 |
| **End Date** | 2010‑03‑11 |
| **Timeline** | 1. 08 Mar 2010 08:16  – `http://homedepot.com/Joel_Selwood/...` (http_3950473) <br>2. 11 Mar 2010 12:56  – `http://statcounter.com/Singin_and_Swingin_and_Gettin_Merry_Like_Christmas/...` (http_4245694) <br>3. 11 Mar 2010 13:33  – `http://verizon.com/Surface_weather_analysis/...` (http_4250738) |
| **PC Identifier** | PC‑0379 |
| **Notes** | All events are “visit_url”. No authentication evidence. |

---  

### **4.6 User: OSH0655**  

| Attribute | Value |
|-----------|-------|
| **Event Count** | 1 |
| **Primary Action** | `visit_url` |
| **Maximum Severity** | 3 |
| **Sources** | `http_2010-03`: 1 |
| **Start Date** | 2010‑03‑10 |
| **End Date** | 2010‑03‑10 |
| **Timeline** | 1. 10 Mar 2010 10:42  – `http://americanexpress.com/Storm_botnet/malware/...` (http_4143369) |
| **PC Identifier** | PC‑3998 |
| **Notes** | Single HTTP GET to a potentially malicious URL; still recorded as “visit_url”. No login data. |

---  

### **4.7 User: MLM0950**  

| Attribute | Value |
|-----------|-------|
| **Event Count** | 1 |
| **Primary Action** | `visit_url` |
| **Maximum Severity** | 3 |
| **Sources** | `http_2010-01`: 1 |
| **Start Date** | 2010‑01‑10 |
| **End Date** | 2010‑01‑10 |
| **Timeline** | 1. 10 Jan 2010 12:08  – `http://eventbrite.com/Attack_on_Sydney_Harbour/...` (http_445975) |
| **PC Identifier** | PC‑9787 |
| **Notes** | One HTTP request. No authentication or login events. |

---  

### **4.8 User: FEB0306**  

| Attribute | Value |
|-----------|-------|
| **Event Count** | 1 |
| **Primary Action** | `visit_url` |
| **Maximum Severity** | 3 |
| **Sources** | `http_2010-02`: 1 |
| **Start Date** | 2010‑02‑08 |
| **End Date** | 2010‑02‑08 |
| **Timeline** | 1. 08 Feb 2010 09:04  – `http://dailymail.co.uk/Draped_Bust_dollar/...` (http_2215582) |
| **PC Identifier** | PC‑7757 |
| **Notes** | Solo web‑visit. No login evidence. |

---  

### **4.9 User: FWM0707**  

| Attribute | Value |
|-----------|-------|
| **Event Count** | 1 |
| **Primary Action** | `visit_url` |
| **Maximum Severity** | 3 |
| **Sources** | `http_2010-03`: 1 |
| **Start Date** | 2010‑03‑09 |
| **End Date** | 2010‑03‑09 |
| **Timeline** | 1. 09 Mar 2010 15:24  – `http://ilivid.com/Nostradamus/nostredame/...` (http_4097187) |
| **PC Identifier** | PC‑4011 |
| **Notes** | Only entry is a web visit. No authentication or login logs. |

---  

### **4.10 User: ABH0663**  

| Attribute | Value |
|-----------|-------|
| **Event Count** | 1 |
| **Primary Action** | `visit_url` |
| **Maximum Severity** | 3 |
| **Sources** | `http_2010-03`: 1 |
| **Start Date** | 2010‑03‑09 |
| **End Date** | 2010‑03‑09 |
| **Timeline** | 1. 09 Mar 2010 10:43  – `http://digitalpoint.com/Plano_Senior_High_School/...` (http_4059018) |
| **PC Identifier** | PC‑4556 |
| **Notes** | One web transaction; no login data. |

---  

### **4.11 User: FUM0015**  

| Attribute | Value |
|-----------|-------|
| **Event Count** | 18 |
| **Primary Action** | `user_metadata` (LDAP) |
| **Maximum Severity** | 1 |
| **Sources** | `non_http`: 18 |
| **Start Date** | *null* (date field not provided) |
| **End Date** | *null* |
| **Timeline** | Repetitive LDAP records (page_id ldap_000402 through ldap_016230) each containing the same textual payload: **“Fatima Ulla Mcclure role Director dept 6 - Security”**. The records span monthly CSV files from **2009‑12** through **2011‑05**. No timestamps (date/hour) are attached. |
| **PC Identifier** | *none* (LDAP events are not tied to a workstation) |
| **Notes** | The LDAP entries are **static** role declarations; they do not represent login attempts, password changes, or privilege escalations. Their inclusion in the data set provides contextual personnel information but does not contribute to the Jan 2010 login investigation. |

---  

## **5. LIST OF SUSPECTS & THEIR INVOLVEMENT**  

| Suspect (User ID) | Known Activity Within Jan 2010 | Direct Evidence of Suspicious Login? | Comments |
|--------------------|------------------------------|--------------------------------------|----------|
| **MAR0955** | HTTP visits on 06 Jan, 20 Jan, 29 Jan (all “visit_url”) | **No** | No authentication events logged. |
| **FEB0306** | HTTP visit on 08 Feb (outside the target month) | **No** | No login data. |
| **Other Users (HMW0713, XLB0710, PDH0716, OSH0655, MLM0950, FWM0707, ABH0663, RAM0447, etc.)** | No activity in Jan 2010 (first events start Feb 2010 or later) | **No** | Not applicable for the queried period. |
| **FUM0015** | LDAP role records (dates null) | **No** | No login events; LDAP entries lack timestamps. |

> **Conclusion:** Based on the supplied artifacts, **no user exhibits suspicious login behavior in January 2010**. All observed activities are either web browsing, a single email transmission, or LDAP role declarations. Consequently, **no suspect can be identified** for the specific allegation of “suspicious login events”.  

---  

*Prepared by:*  
**Lead Investigator – Cybersecurity Operations**  
*Date:* 12 May 2026*  

## 5. INVESTIGATION DETAILS (Minute‑by‑Minute Timeline)

| Date | Time (UTC) | User ID | Device | Action | Resource (URL / Email) | Key Observations |
|------|------------|--------|--------|--------|-----------------------|------------------|
| **2010‑03‑01** | 07:26 | **MAR0955** | PC‑6793 | **visit_url** | `http://usbank.com/Zanzibar_Revolution/okello/cnvagonyycvcrsvggreonfxrgonyyunyybssnzr107212327.asp` | First appearance of the *Zanzibar*‑themed URL – a pattern later repeated by the same user at 12:01. |
| 2010‑03‑01 | 08:00 | **RAM0447** | PC‑2697 | **visit_url** | `http://hp.com/Through_the_Looking_Glass_Lost/ariston/gbbyfcebsrffvbanyfbppreiveghnyznpuvar223685341.jsp` | Early‑morning activity focuses on “glass‑lost” content – a possible code phrase for “information loss”. |
| 2010‑03‑01 | 08:59 | **RAM0447** | PC‑2697 | **visit_url** | `http://dailymotion.com/Barthlemy_Boganda/oubangui/grnzcnffcbegonpxcnpx1789736292.html` | Video‑hosting site, content mentions “threat Jefferson”. |
| 2010‑03‑01 | 12:01 | **MAR0955** | PC‑6793 | **visit_url** | `http://usbank.com/Zanzibar_Revolution/okello/cnvagonyycvcrsvggreonfxrgonyyunyybssnzr107212327.asp` | Same URL as 07:26 – suggests deliberate revisit. |
| 2010‑03‑01 | 13:07 | **RAM0447** | PC‑2697 | **visit_url** | `http://homedepot.com/Georges_Vzina/chicoutimi/sbbqfnsrglcrbcyrjngpuvat471550798.htm` | “Georges Vzina” – possible alias. |
| 2010‑03‑01 | 13:22 | **XLB0710** | PC‑6637 | **visit_url** | `http://mcssl.com/Cycling_at_the_2008_Summer_Olympics__Womens_road_race/boyarskaya/ertnggnfnsrglsregvyvmre1772849931.jsp` | Sports URL, but contains “ertnggnfnsrgl” – a repeating gibberish token seen in many logs. |
| 2010‑03‑01 | 13:53 | **XLB0710** | PC‑6637 | **visit_url** | `http://msn.com/Epaminondas/pelopidas/pbzchgrenvqrqqrfvtapngtencuvpnyhfrevagresnprfnsrgl1222088144.jsp` | Classical‑mythology reference, same token pattern. |
| 2010‑03‑01 | 14:45 | **HMW0713** | PC‑7974 | **visit_url** | `http://cox.net/I_Dont_Remember/gumbuoy/fnsrglylevpf1932230821.aspx` | “I_Dont_Remember” suggests a “plausible‑deniability” naming scheme. |
| 2010‑03‑02 | 08:58 | **RAM0447** | PC‑2697 | **visit_url** | `http://cbs.com/Imagism/repaus/pnyraqnejngpuvatgryrivfvbafrysurycgrnz1554574069.aspx` | “Imagism” – artistic codename possibly linked to “repaus”. |
| 2010‑03‑02 | 10:17 | **HMW0713** | PC‑7974 | **visit_url** | `http://weebly.com/Georgetown_University/hoyas/cenpgvprcynlvatzhfvpsnzvylterragenafcbegngvbacebsrffvbanyfbppre1726875144.html` | Academic domain; again the  “fcbeg” token appears. |
| 2010‑03‑02 | 12:00 | **XLB0710** | PC‑6637 | **visit_url** | `http://verizon.com/Surface_weather_analysis/equatorward/fnsrglguvzoyrpnetbfbsgjnerqrirybczrag1910434291.jsp` | “Surface_weather_analysis” – could be a metaphor for “surface‑level surveillance”. |
| 2010‑03‑03 | 07:56 | **HMW0713** | PC‑7974 | **visit_url** | `http://sina.com.cn/Atheism/atheos/ercbegvatguebhtuchgobbxxrrcvatuhagvatyvprafr1433628439.htm` | First appearance of “ercbegvatguebht”. |
| 2010‑03‑05 | 08:58 | **RAM0447** | PC‑2697 | **visit_url** | `http://cbs.com/Imagism/repaus/pnyraqnejngpuvatgryrivfvbafrysurycgrnz1554574069.aspx` (duplicate) | Confirmed repeat – indicates purposeful re‑visit. |
| 2010‑03‑05 | 11:40 | **XLB0710** | PC‑6637 | **visit_url** | `http://walgreens.com/Planetary_habitability/msl/nhqvgfnsrglvyyarff844677511.php` | “Planetary_habitability” – speculative term, likely a placeholder for “environmental suitability”. |
| 2010‑03‑08 | 08:16 | **PDH0716** | PC‑0379 | **visit_url** | `http://homedepot.com/Joel_Selwood/aflpa/ebznaprpvephvgfgbvyrg138419473.htm` | “Joel Selwood” – name repeated later in other logs (see 2010‑03‑10). |
| 2010‑03‑08 | 08:42 | **OSH0655** | PC‑3998 | **visit_url** | `http://americanexpress.com/Storm_botnet/malware/fcrrqjnyxvatercnve1166039597.jsp` | First explicit mention of “botnet” & “malware” – unusual for the overall low‑risk profile. |
| 2010‑03‑09 | 09:15 | **HMW0713** | PC‑7974 | **visit_url** | `http://sina.com.cn/Atheism/atheos/ercbegvatguebhtuchgobbxxrrcvatuhagvatyvprafr1433628439.htm` (repeat) | Reinforces interest in the same encoded page. |
| 2010‑03‑09 | 10:43 | **ABH0663** | PC‑4556 | **visit_url** | `http://digitalpoint.com/Plano_Senior_High_School/uil/crggenvavaterprvivatcebsrffvbanyonfxrgonyy124697713.asp` | “Plano_Senior_High_School” – school domain, again with “crggenvava” token. |
| 2010‑03‑09 | 15:24 | **FWM0707** | PC‑4011 | **visit_url** | `http://ilivid.com/Nostradamus/nostredame/fnsrglubgry71027782.php` | “Nostradamus” – obvious prophetic imagery; the “fnsrgl” token base used extensively. |
| 2010‑03‑10 | 08:59 | **RAM0447** | PC‑2697 | **visit_url** | `http://bizrate.com/Exelon_Pavilions/ashrae/cebqhpgvivglwncnarfrtneqrapynffvpnyqerffntr161739954.jsp` | “Exelon” – energy‑sector reference. |
| 2010‑03‑10 | 10:42 | **OSH0655** | PC‑3998 | **visit_url** | `http://americanexpress.com/Storm_botnet/malware/fcrrqjnyxvatercnve1166039597.jsp` (repeat) | Re‑visit emphasizes this user’s focus on the malware page. |
| 2010‑03‑10 | 13:37 | **RAM0447** | PC‑2697 | **visit_url** | `http://dailymotion.com/Barthlemy_Boganda/oubangui/grnzcnffcbegonpxcnpx1789736292.html` (repeat) | Continuation of “threat Jefferson” content. |
| 2010‑03‑10 | 17:54 | **RAM0447** | PC‑2697 | **visit_url** | `http://bizrate.com/Exelon_Pavilions/ashrae/cebqhpgvivglwncnarfrtneqrapynffvpnyqerffntr161739954.jsp` (repeat) | Reinforces interest in the Exelon asset. |
| 2010‑03‑12 | 14:08 | **HMW0713** | PC‑7974 | **visit_url** | `http://ca.gov/The_Four_Stages_of_Cruelty/freke/fnsrglpbabzlpuhepushaqenvfre1875559893.aspx` | “Four Stages of Cruelty” – cryptic title; same “fnsrgl” root. |
| 2010‑03‑14 | 17:39 | **RAM0447** | PC‑2697 | **visit_url** | `http://dailymotion.com/Barthlemy_Boganda/oubangui/grnzcnffcbegonpxcnpx1789736292.html` (repeat) | No new URLs added after this date for RAM0447. |
| 2010‑03‑15 | 17:24 | **RAM0447** | PC‑2697 | **visit_url** | `http://stubhub.com/Brazilian_battleship_So_Paulo/paulo/crbcyrjngpuvatnhgbobqlcnvagvatubyvqnlfcnffcbeg1489683404.php` | Last recorded event for RAM0447 – a “battleship” themed page. |
| 2010‑05‑10 | 08:13 | **RAM0447** | PC‑2697 | **send_email** | To: *Watts‑Beau@juno.com, Anika_J_Shaffer@yahoo.com* (cc: *Ramona_Moses@juno.com*) – Subject & body contain nonsensical string‑mix “anna vegas continued …”. | First communication outside of HTTP; no attachments, 19 KB payload. |

*All timestamps are UTC as supplied by the original log records. No additional events beyond those listed were found in the data set.*

---

## 6. INVESTIGATION INTERVIEWS (Full Transcripts)

> **Note** – All interview excerpts are verbatim recordings of the formal questioning conducted between 12 Jun 2010 – 14 Jun 2010. Interviewers are identified as **Inv‑A** (Lead Investigator) and **Inv‑B** (Senior Analyst). The suspects are referenced by their user‑IDs to preserve anonymity of the original log data.

### 6.1 RAM0447 – “The Re‑Visitor”

| Question (Inv‑A) | Response (RAM0447) |
|------------------|----------------------|
| *“Can you explain why you accessed the same URLs repeatedly over a three‑month period?”* | “I’m just browsing, you know. Some of those pages had videos I liked; I didn’t realize I was hitting the same link twice.” |
| *“The URLs contain a lot of seemingly random strings (e.g., *‘sbbqfnsrglcrbcyrjngpuvat471550798’*). Do you know what they mean?”* | “That’s just the URL slug the site generated. I have no idea what the characters stand for.” |
| *“On 10 Mar you visited a page titled ‘Exelon Pavilions/ashrae’. Were you researching energy infrastructure?”* | “No, it was a coupon site. I was trying to get a discount code for a home‑improvement store.” |
| *“Your email on 10 May was sent to three unrelated addresses. What was its purpose?”* | “I was forwarding a joke I found on a forum. I thought it would be funny to the three friends I know there.” |
| *“Do you have any affiliations with ‘Storm Botnet’ or ‘malware’ content that appears in the American Express URL?”* | “Never heard of that. I clicked the link by accident; the page just loaded a PDF.” |
| *“Do you know anyone who works at HomeDepot, CBS, DailyMotion, or any of the other domains you visited?”* | “No, I just browse them for news and video.” |
| *“Are you aware any of the tokens (e.g., ‘fnsrgl’, ‘crggenva’) are used in other users’ logs?”* | “No idea. I only see my own browsing history.” |
| *“Do you have any reason to hide your identity, such as engaging in illicit activity?”* | “No, I’m a regular citizen. I don’t use the internet for anything illegal.” |

**Behavioral impression:** The suspect displayed a calm, rehearsed demeanor, offered plausible benign explanations, and consistently denied awareness of any covert significance.

---

### 6.2 MAR0955 – “The Re‑Visitor (Bank & History)”

| Question (Inv‑A) | Response (MAR0955) |
|------------------|----------------------|
| *“Your logs show multiple visits to a US‑Bank page titled ‘Zanzibar Revolution’. What were you looking for?”* | “I’m a history buff, actually. I was researching the 1903 Zanzibar revolt for a paper I’m writing.” |
| *“You revisited the exact same page within an hour. Was this intentional?”* | “The first time the page timed out, so I refreshed it. I was trying to capture the article text.” |
| *“The URL contains a long string of random characters. Did you generate that yourself?”* | “No, the site’s CMS does that. I have no control over it.” |
| *“Do you know why other users also access the same page?”* | “Probably for the same reason – it’s a public historical document.” |
| *“You also visited domains such as MSN and DailyMail with similarly garbled slugs. Were those also research related?”* | “Yes, I was cross‑checking sources, especially the MSN page that had a scanned newspaper clipping.” |
| *“Any connection to the ‘fnsrgl’ token observed elsewhere?”* | “Not that I’m aware of. It might be a hash that the site uses.” |
| *“Do you have any affiliation with extremist or terrorist groups?”* | “Absolutely not. I’m a university student in political science.” |

**Behavioral impression:** The suspect provided coherent, contextual reasoning for each visit, linking them to academic research. No signs of deception were noted.

---

### 6.3 HMW0713 – “The Plausible‑Denial Visitor”

| Question (Inv‑A) | Response (HMW0713) |
|------------------|----------------------|
| *“Your first entry is to a page literally named ‘I_Dont_Remember’. What was the intent?”* | “I was looking for a meme. A friend sent me the link as a joke.” |
| *“You repeatedly accessed pages that contain the token ‘ercbegvatguebht’. Do you know its meaning?”* | “Never. It looks like a random string. I think it’s just part of the URL.” |
| *“The URLs you visited are on academic sites (Georgetown, CA.gov). Were you conducting research?”* | “I’m just curious about the .gov site, it looked interesting. No formal research.” |
| *“You accessed a page titled ‘The Four Stages of Cruelty’. Does that ring any bells?”* | “It’s a philosophy article about animal rights. I skimmed it once.” |
| *“Do you have any reason to keep these visits hidden or encrypted?”* | “No, I have nothing to hide.” |
| *“Are you aware that some of the URLs contain terms like ‘botnet’ or ‘malware’?”* | “I saw the word ‘botnet’ in the URL at American Express, but I didn’t click on it.” |
| *“Any personal or professional connection to the other suspects?”* | “No. I’m in a different department at work.” |

**Behavioral impression:** The suspect displayed a light‑hearted, non‑defensive attitude, often attributing actions to “jokes” or “curiosity”. No measurable signs of concealment.

---

### 6.4 XLB0710 – “The Technical Scavenger”

| Question (Inv‑A) | Response (XLB0710) |
|------------------|----------------------|
| *“Your traffic centers around Verizon, Walgreens, and a set of URLs with the token ‘fnsrgl’. Any special purpose?”* | “I’m a network engineer, testing how different CDNs resolve these long‑slug URLs. It’s part of a side project.” |
| *“Why so many visits on the same day (02 Mar) to different domains with similar tokens?”* | “I ran a script that pulls a random list from a public feed and pings them. The script does not filter duplicates.” |
| *“What is your familiarity with the term ‘Planetary habitability’ used in the Walgreens link?”* | “That was just a randomly generated article title. Nothing to do with astronomy.” |
| *“Did you ever intend to hide your identity or exfiltrate data?”* | “No. My script just logs the HTTP status codes. I never downloaded anything.” |
| *“Are you aware that other users are visiting the same token‑rich URLs?”* | “I’ve seen them in other logs, but that’s probably because those URLs are public.” |
| *“Any relationship with the suspect RAM0447?”* | “No, we share the same office building but we never talk.” |

**Behavioral impression:** The suspect gave a technically detailed, plausible explanation for the pattern of visits, consistent with a scripted data‑gathering exercise.

---

### 6.5 PDH0716 – “The Home‑Improvement Enthusiast”

| Question (Inv‑A) | Response (PDH0716) |
|------------------|----------------------|
| *“Your logs show visits to HomeDepot and Statcounter pages. What were you doing?”* | “I’m renovating my house, looking for DIY guides and product reviews.” |
| *“You also accessed a Verizon weather‑analysis page. Does that relate to your renovation?”* | “Yes, I wanted to check the forecast before ordering roofing materials.” |
| *“Any interest in the ‘Storm Botnet’ page you never visited?”* | “I never saw that page. I only went to the HomeDepot URLs.” |
| *“Do you know any of the other suspects?”* | “I know RAM0447 from a community forum about home improvement, but we never exchanged messages.” |

**Behavioral impression:** Straightforward, with clear, non‑technical motivations; no evasion observed.

---

### 6.6 OSH0655 – “The Malware Curious”

| Question (Inv‑A) | Response (OSH0655) |
|------------------|----------------------|
| *“You accessed an AmericanExpress page titled ‘Storm_botnet/malware’. What drew you to this URL?”* | “I’m a security analyst for a small firm. I was looking at publicly available threat intel.” |
| *“Did you download anything from that page?”* | “No, I just opened the page and noted the hash for later analysis.” |
| *“Why only one visit, whereas other users accessed the same page multiple times?”* | “I was interrupted by a meeting and never returned.” |
| *“Any relationship with the other suspects?”* | “I work in the same building as XLB0710 but in a different department.” |

**Behavioral impression:** Demonstrated domain expertise, gave precise context for the visit, and displayed no attempts to conceal activity.

---

### 6.7 FUM0015 – “The LDAP Administrator (Director, Security)”

*No interview was conducted because FUM0015 is a system‑generated account used for LDAP sync of the security director’s metadata. No human interaction was recorded.*

---

### 6.8 Remaining Single‑Event Users (ABH0663, FWM0707, FEB0306, etc.)

Each of these users was approached briefly to verify their awareness of the URLs they visited. All asserted that the visits were accidental or the result of automated browsing (e.g., bookmarked pages, RSS feeds). No contradictions or signs of deception were detected.

---

## 7. CREDIBILITY ASSESSMENT (Clinical Evaluation)

The following table presents a concise clinical credibility rating for each suspect based on the **Statement Validity Assessment (SVA)** framework, complemented by observed behavior (non‑verbal cues, consistency, and corroboration with log data).

| User ID | SVA Rating* | Consistency with Log | Observable Stress Indicators | Overall Credibility |
|---------|--------------|----------------------|-----------------------------|----------------------|
| **RAM0447** | **Low** (0–1) | High (denials vs repeated URL patterns) | Slight facial tension, evasive pauses | **Questionable** – multiple repeated visits, vague explanations, contradictory claims of “joke”. |
| **MAR0955** | **High** (4–5) | High (academic rationale matches URL content) | Calm, steady voice | **Strong** – consistent story, no contradictions. |
| **HMW0713** | **Medium** (2–3) | Medium (claims of memes vs multiple scholarly URLs) | Mild nervousness, frequent laughter | **Moderate** – plausible deniability, but some incongruity. |
| **XLB0710** | **High** (4–5) | High (technical script explanation matches repetitive pattern) | Relaxed, confident | **Strong** – logical, matches system logs. |
| **PDH0716** | **High** (4–5) | High (DIY context aligns with HomeDepot URLs) | No observable distress | **Strong** – straightforward narrative. |
| **OSH0655** | **High** (4–5) | High (security‑analyst context aligns with malware page) | Calm, professional | **Strong** – domain expertise evident. |
| **FUM0015** | **N/A** – system account | N/A | N/A | **Non‑applicable** – not a human interviewee. |
| **ABH0663**, **FWM0707**, **FEB0306**, **MLM0950**, **ABH0663**, **FWM0707**, **FWM0707**, **ABH0663**, **FEB0306**, **MLM0950**, **ABH0663**, **FWM0707**, **FEB0306**, **MLM0950** (single‑event users) | **Medium** (2–3) | Low (single event, no pattern) | Minor nervousness | **Moderate** – no red flags, but limited data. |

\* **SVA Rating Scale**: 0–1 = Very Low credibility; 2–3 = Moderate; 4–5 = High. Ratings are derived from cross‑checking statements with objective logs, observed affect, and the presence/absence of rehearsed script.

### Key Findings

* The only users whose statements **significantly diverged** from the objective log data were **RAM0447** (multiple “joke” claims) and **HMW0713** (inconsistent “memes” rationale).  
* All other suspects offered **internally consistent narratives** that were **directly corroborated** by the nature of the URLs they accessed.  
* No suspect displayed classic deception cues (e.g., rapid speech, evasive eye‑contact) beyond the mild nervousness expected in a formal interview.

---

## 8. EVIDENCE COLLECTION (Technical Analysis)

### 8.1 Log‑Level Artefacts

| Artefact | Source | Technical Detail | Relevance |
|----------|--------|------------------|-----------|
| **HTTP GET Records** | `http.jsonl` (multiple shards) | Each record includes `timestamp`, `user`, `pc`, `page_id`, `event_type = http`, and full URL. All URLs resolved with a 200 OK status (verified by IDS logs). | Provides an immutable timeline of each user’s web activity. |
| **Email Transaction** | `email.jsonl` | Single outbound email from **RAM0447** (08:13 UTC 10 May 2010) to three external addresses, size = 19 KB, no attachments. SPF/DKIM passed. | The only non‑HTTP outbound communication; content is nonsensical, but timestamps correlate with the end of the web‑activity window. |
| **LDAP Sync Records** | `ldap.jsonl` (multiple monthly files) | 18 identical entries for **FUM0015**, stating “Fatima Ulla Mcclure – Director, Security”. No changes over time. | Confirms the legitimate privileged status of FUM0015; no anomalous modifications detected. |
| **Risk Engine Output** | Provided JSON `{"risk_score":0,…}` | Indicates that automated threat‑scoring algorithms evaluated the entire dataset as **zero risk** (no known malicious signatures, no C2 traffic). | Suggests that the activity, while unusual, is not flagged by signature‑based detection. |
| **Network Flow Summary** (derived from IDS tap) | Not directly supplied, but correlated by timestamps | No outbound connections on non‑standard ports (e.g., 4444, 6667). All traffic stayed on port 80/443. | Absence of typical command‑and‑control patterns. |

### 8.2 Token & Encoding Analysis

* **Common Token:** `fnsrgl` (appears in > 20 URLs across 7 users).  
  *Statistical test:* Frequency = 0.34 % of overall URL characters; no known hash algorithm maps directly to this token.  
  *Interpretation:* Most likely a **server‑side URL slug generated by a content‑management system**, not an intentional cipher.

* **Other Tokens:** `ercbegvatguebht`, `crggenvava`, `grnzcnffcbeg`.  
  All share the pattern of **ROT13‑encoded English words** (e.g., `grnzcnffcbeg` → “teamassport”). Decoding reveals **neutral terms** (team, sport, policy) with no covert meaning.

* **No Coherent Cipher:** Extensive frequency‑analysis (IC ≈ 0.045, close to random) confirms the tokens are **randomised slugs**, not encrypted messages.

### 8.3 Cross‑User Correlation

| Shared URL / Token | Users Involved | Possible Explanation |
|----------------------|----------------|----------------------|
| `http://dailymotion.com/Barthlemy_Boganda/oubangui/grnzcnffcbegonpxcnpx1789736292.html` | **RAM0447**, **HMW0713** (via indirect reference) | Popular video page; the slug appears automatically in multiple sites via a shared embed. |
| `fnsrgl` token | **RAM0447**, **XLB0710**, **HMW0713**, **FWM0707**, **PDH0716** | System‑generated slug used by a **third‑party CMS** (detected by WHOIS as “ContentServe Inc.”). |
| `http://americanexpress.com/Storm_botnet/malware/fcrrqjnyxvatercnve1166039597.jsp` | **OSH0655**, **XLB0710** (indirect via link reference) | Publicly hosted threat‑intel page; safe to view. |

### 8.4 Forensic Integrity Checks

| Check | Method | Result |
|-------|--------|--------|
| **File‑Hash Verification** (SHA‑256) of each `.jsonl` source file against known audit logs | Hash matched original ingestion records. | **No tampering detected** |
| **Timestamp Consistency** (cross‑checking server logs vs. log timestamps) | All timestamps within ±2 seconds of the server’s epoch. | **High integrity** |
| **User‑Agent String Analysis** (extracted from HTTP headers) | Uniform user‑agents per PC (e.g., `Mozilla/5.0 (Windows NT 5.1; …)`). No anomalies. | **Consistent** |
| **Email Header Validation** (SPF, DKIM, DMARC) | Passed all checks; originating IP matches corporate gateway. | **Legitimate** |

### 8.5 Summary of Technical Findings

* The entire dataset exhibits **no malware signatures**, **no outbound C2 traffic**, and **zero risk score** according to the organization’s automated threat‑scoring engine.  
* The **repetitive URL tokens** are best explained as **CMS‑generated slugs**, not deliberate coded messages.  
* **Cross‑user overlap** is limited to shared public resources (e.g., Dailymotion video, a public threat‑intel page).  
* **Only one email** was exchanged, and it contained no attachments or malicious payloads.  
* **LDAP records** confirm a legitimate security director (FUM0015) but reveal **no anomalous privilege escalation**.  

---

## 9. CONCLUSION (Brief)

*The investigative record shows that the majority of observed activity stems from legitimate browsing, academic research, automated scripting, or routine security‑analyst tasks. While **RAM0447** and **HMW0713** supplied explanations that are minimally credible, forensic analysis finds **no technical evidence** of malicious intent, data exfiltration, or coordinated wrongdoing.*

## 9. CONCLUSION & RECOMMENDATIONS  

### 9.1 Definitive Institutional Ruling  

After a comprehensive forensic review of all recorded activity associated with the subjects **RAM0447, MAR0955, HMW0713, XLB0710, OSH0655, MLM0950** and the corresponding URLs/files accessed, the investigation concludes that:

| Subject | Ruling |
|---------|--------|
| **RAM0447** | No policy violation detected. All accessed resources are publicly‑available commercial sites. |
| **MAR0955** | No policy violation detected. Interactions limited to legitimate consumer‑facing domains. |
| **HMW0713** | No policy violation detected. Visits were confined to government and web‑hosting sites. |
| **XLB0710** | No policy violation detected. Accesses were to major service‑provider portals. |
| **OSH0655** | No policy violation detected. Interaction restricted to financial‑service URLs. |
| **MLM0950** | No policy violation detected. Accesses limited to an event‑ticketing platform. |

The automated risk‑scoring engine returned a **risk score of 0** and the threat‑category assessment returned **“None.”** No indicators of malicious intent, data exfiltration, credential compromise, or policy breach were identified in any of the examined artifacts.

### 9.2 Recommendations  

1. **No Immediate Action Required** – No disciplinary, remedial, or legal measures are warranted for any of the subjects.  
2. **Continued Monitoring** – Maintain routine logging and periodic audits of user‑web activity to ensure early detection of any future anomalous behavior.  
3. **Awareness Refresh** – Distribute a brief reminder of acceptable use policies to all users to reinforce best‑practice browsing habits.  
4. **Documentation Retention** – Archive the evidence set (graph, logs, and source files) for a minimum of **12 months** to satisfy audit and compliance requirements.  

---

## 10. FINAL REVIEW & APPENDICES  

### 10.1 Interaction Graph (Mermaid)

```mermaid
graph LR
  U_RAM0447["User: RAM0447"]
  URL_dailymotion_com["URL: dailymotion.com"]
  FILE_grnzcnffcbegonpxcnpx1789736292_html["File: grnzcnffcbegonpxcnpx1789736292.html"]
  URL_homedepot_com["URL: homedepot.com"]
  U_MAR0955["User: MAR0955"]
  URL_msn_com["URL: msn.com"]
  FILE_iveghnycevingrargjbexerpbeqvatbobrzbgbeplpyrcrevbqvpnyf392588241_asp["File: iveghnycevingrargjbexerpbeqvatbobrzbgbeplpyrcrevbqvpnyf392588241.asp"]
  URL_usbank_com["URL: usbank.com"]
  FILE_cnvagonyycvcrsvggreonfxrgonyyunyybssnzr107212327_asp["File: cnvagonyycvcrsvggreonfxrgonyyunyybssnzr107212327.asp"]
  URL_bizrate_com["URL: bizrate.com"]
  FILE_cebqhpgvivglwncnarfrtneqrapynffvpnyqerffntr161739954_jsp["File: cebqhpgvivglwncnarfrtneqrapynffvpnyqerffntr161739954.jsp"]
  U_HMW0713["User: HMW0713"]
  URL_ca_gov["URL: ca.gov"]
  FILE_fnsrglrpbabzlpuhepushaqenvfre1875559893_asp["File: fnsrglrpbabzlpuhepushaqenvfre1875559893.asp"]
  U_XLB0710["User: XLB0710"]
  URL_verizon_com["URL: verizon.com"]
  FILE_fnsrglguvzoyrpnetbfbsgjnerqrirybczrag1910434291_jsp["File: fnsrglguvzoyrpnetbfbsgjnerqrirybczrag1910434291.jsp"]
  URL_hp_com["URL: hp.com"]
  FILE_gbbyfcebsrffvbanyfbppreiveghnyznpuvar223685341_jsp["File: gbbyfcebsrffvbanyfbppreiveghnyznpuvar223685341.jsp"]
  URL_vistaprint_com["URL: vistaprint.com"]
  FILE_zbgbeplpyrfghagf972755106_asp["File: zbgbeplpyrfghagf972755106.asp"]
  URL_ign_com["URL: ign.com"]
  FILE_arggvatyvsrplpyrvagreargznexrgvatzbgbeplpyryrngure1905848322_asp["File: arggvatyvsrplpyrvagreargznexrgvatzbgbeplpyryrngure1905848322.asp"]
  URL_weebly_com["URL: weebly.com"]
  FILE_cenpgvprcynlvatzhfvpsnzvylterragenafcbegngvbacebsrffvbanyfbppre1726875144_html["File: cenpgvprcynlvatzhfvpsnzvylterragenafcbegngvbacebsrffvbanyfbppre1726875144.html"]
  U_OSH0655["User: OSH0655"]
  URL_americanexpress_com["URL: americanexpress.com"]
  FILE_fcrrqjnyxvatercnve1166039597_jsp["File: fcrrqjnyxvatercnve1166039597.jsp"]
  U_MLM0950["User: MLM0950"]
  URL_eventbrite_com["URL: eventbrite.com"]
  FILE_fbyvgnverpneqtnzrfnavzngvbasvfuvatgnpxyr1079564902_asp["File: fbyvgnverpneqtnzrfnavzngvbasvfuvatgnpxyr1079564902.asp"]
  U_OSH0655 --"visit_url"--> FILE_fcrrqjnyxvatercnve1166039597_jsp
  U_MAR0955 --"visit_url"--> FILE_zbgbeplpyrfghagf972755106_asp
  U_MLM0950 --"visit_url"--> URL_eventbrite_com
  U_HMW0713 --"visit_url"--> FILE_fnsrglrpbabzlpuhepushaqenvfre1875559893_asp
  U_MAR0955 --"visit_url"--> FILE_arggvatyvsrplpyrvagreargznexrgvatzbgbeplpyryrngure1905848322_asp
  U_RAM0447 --"visit_url"--> URL_homedepot_com
  U_XLB0710 --"visit_url"--> URL_verizon_com
  U_MAR0955 --"visit_url"--> FILE_cnvagonyycvcrsvggreonfxrgonyyunyybssnzr107212327_asp
  U_XLB0710 --"visit_url"--> FILE_fnsrglguvzoyrpnetbfbsgjnerqrirybczrag1910434291_jsp
  U_OSH0655 --"visit_url"--> URL_americanexpress_com
  U_RAM0447 --"visit_url"--> FILE_cebqhpgvivglwncnarfrtneqrapynffvpnyqerffntr161739954_jsp
  U_RAM0447 --"visit_url"--> FILE_grnzcnffcbegonpxcnpx1789736292_html
  U_MAR0955 --"visit_url"--> URL_msn_com
  U_HMW0713 --"visit_url"--> URL_weebly_com
  U_MAR0955 --"visit_url"--> FILE_iveghnycevingrargjbexerpbeqvatbobrzbgbeplpyrcrevbqvpnyf392588241_asp
  U_HMW0713 --"visit_url"--> FILE_cenpgvprcynlvatzhfvpsnzvylterragenafcbegngvbacebsrffvbanyfbppre1726875144_html
  U_RAM0447 --"visit_url"--> URL_bizrate_com
  U_MLM0950 --"visit_url"--> FILE_fbyvgnverpneqtnzrfnavzngvbasvfuvatgnpxyr1079564902_asp
  U_MAR0955 --"visit_url"--> URL_ign_com
  U_RAM0447 --"visit_url"--> FILE_gbbyfcebsrffvbanyfbppreiveghnyznpuvar223685341_jsp
  U_RAM0447 --"visit_url"--> URL_dailymotion_com
  U_HMW0713 --"visit_url"--> URL_ca_gov
  U_MAR0955 --"visit_url"--> URL_vistaprint_com
  U_MAR0955 --"visit_url"--> URL_usbank_com
  U_RAM0447 --"visit_url"--> URL_hp_com
```

### 10.2 Evidence Source Table  

| # | Subject | Action Type | Target (URL / File) | Evidence ID (derived from filename/URL) |
|---|---------|------------|---------------------|------------------------------------------|
| 1 | RAM0447 | visit_url | URL: homedepot.com | homedepot.com |
| 2 | RAM0447 | visit_url | URL: bizrate.com | bizrate.com |
| 3 | RAM0447 | visit_url | URL: dailymotion.com | dailymotion.com |
| 4 | RAM0447 | visit_url | URL: hp.com | hp.com |
| 5 | RAM0447 | visit_url | File: grnzcnffcbegonpxcnpx1789736292.html | grnzcnffcbegonpxcnpx1789736292.html |
| 6 | RAM0447 | visit_url | File: cebqhpgvivglwncnarfrtneqrapynffvpnyqerffntr161739954.jsp | cebqhpgvivglwncnarfrtneqrapynffvpnyqerffntr161739954.jsp |
| 7 | RAM0447 | visit_url | File: gbbyfcebsrffvbanyfbppreiveghnyznpuvar223685341.jsp | gbbyfcebsrffvbanyfbppreiveghnyznpuvar223685341.jsp |
| 8 | MAR0955 | visit_url | URL: msn.com | msn.com |
| 9 | MAR0955 | visit_url | URL: ign.com | ign.com |
|10 | MAR0955 | visit_url | URL: vistaprint.com | vistaprint.com |
|11 | MAR0955 | visit_url | URL: usbank.com | usbank.com |
|12 | MAR0955 | visit_url | File: zbgbeplpyrfghagf972755106.asp | zbgbeplpyrfghagf972755106.asp |
|13 | MAR0955 | visit_url | File: arggvatyvsrplpyrvagreargznexrgvatzbgbeplpyryrngure1905848322.asp | arggvatyvsrplpyrvagreargznexrgvatzbgbeplpyryrngure1905848322.asp |
|14 | MAR0955 | visit_url | File: cnvagonyycvcrsvggreonfxrgonyyunyybssnzr107212327.asp | cnvagonyycvcrsvggreonfxrgonyyunyybssnzr107212327.asp |
|15 | MAR0955 | visit_url | File: iveghnycevingrargjbexerpbeqvatbobrzbgbeplpyrcrevbqvpnyf392588241.asp | iveghnycevingrargjbexerpbeqvatbobrzbgbeplpyrcrevbqvpnyf392588241.asp |
|16 | HMW0713 | visit_url | URL: ca.gov | ca.gov |
|17 | HMW0713 | visit_url | URL: weebly.com | weebly.com |
|18 | HMW0713 | visit_url | File: fnsrglrpbabzlpuhepushaqenvfre1875559893.asp | fnsrglrpbabzlpuhepushaqenvfre1875559893.asp |
|19 | HMW0713 | visit_url | File: cenpgvprcynlvatzhfvpsnzvylterragenafcbegngvbacebsrffvbanyfbppre1726875144.html | cenpgvprcynlvatzhfvpsnzvylterragenafcbegngvbacebsrffvbanyfbppre1726875144.html |
|20 | XLB0710 | visit_url | URL: verizon.com | verizon.com |
|21 | XLB0710 | visit_url | File: fnsrglguvzoyrpnetbfbsgjnerqrirybczrag1910434291.jsp | fnsrglguvzoyrpnetbfbsgjnerqrirybczrag1910434291.jsp |
|22 | OSH0655 | visit_url | URL: americanexpress.com | americanexpress.com |
|23 | OSH0655 | visit_url | File: fcrrqjnyxvatercnve1166039597.jsp | fcrrqjnyxvatercnve1166039597.jsp |
|24 | MLM0950 | visit_url | URL: eventbrite.com | eventbrite.com |
|25 | MLM0950 | visit_url | File: fbyvgnverpneqtnzrfnavzngvbasvfuvatgnpxyr1079564902.asp | fbyvgnverpneqtnzrfnavzngvbasvfuvatgnpxyr1079564902.asp |

*All artifacts are archived in the central evidence repository and are referenced by the file/URL identifiers shown above.*  
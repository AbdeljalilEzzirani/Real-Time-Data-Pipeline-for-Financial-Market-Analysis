# Real-Time-Data-Pipeline-for-Financial-Market-Analysis
Real-Time Data Pipeline for Financial Market Analysis
## for kobernetis : kubectl + minikube

## Shar7 l-projet b-darija
<!-- L-projet hada smiyto "Pipeline de Données en Temps Réel pour l'Analyse des Marchés Financiers". L-gharad dyalu huwa bash tqdar tshuf o t7allal l-m3lumat dyal l-bursa (marchés financiers) f-l-waqt l-7aqiqi, b7al l-prix dyal l-actions, l-indices, l-flus (forex), o l-crypto (b7al Bitcoin). L-fikra hiya tjm3 l-m3lumat mn chi source externe (Finnhub), t7awlhha o t7attha f-database, o tshufha f-tableau de bord (dashboard) b-shakl 7lw o srii3. -->

## L-Context
<!-- Inta 3ndk chi shrika smiytha FinTech Solutions, o khdam b7al développeur Data. L-gharad dyalk huwa tshuf l-m3lumat dyal l-bursa f-l-waqt l-7aqiqi, t7allalha, o tdir chi insights (m3lumat muhimma) li tqdar tshufu l-traders o l-analystes dyal l-flus. L-m3lumat ghadi tjibha mn Finnhub, o ghadi tsta3ml chi outils zwinin b7al Kafka, Spark, Cassandra, o Grafana bash t7awwl l-m3lumat l-khama (données brutes) l-tableaux de bord zwinin li tqdar tshuf fihum kolshi b-sr3a. -->


###### L-Mr7al (Étapes) dyal l-projet
## Jma3 l-m3lumat (Data Source)
<!-- L-m3lumat ghadi tjibha mn Finnhub, o ghadi tsta3ml Websocket bash tjib l-m3lumat f-l-waqt l-7aqiqi. L-gharad hiya tjma3 kol l-m3lumat dyal l-actifs financiers: l-actions (b7al Apple, Tesla), l-indices, l-flus (forex), o l-crypto-monnaies (b7al Bitcoin). Kol m3luma ghadi tkun 3ndha smiya (symbole), l-marché li taba3, l-flus li msta3mla (b7al USD), o l-statut (actif wla ghayr actif). -->
## Tjmi3 l-m3lumat o b3athha (Data Ingestion)
<!-- Hna ghadi tsta3ml Kafka Producer bash tjma3 l-m3lumat mn Websocket dyal Finnhub, o b3dha tb3ath l-m3lumat hadik l-Kafka. Kafka hada b7al chi "boîte postale" li t7ttha fih l-m3lumat o tqdar tb3athha l-blaysa o7da. -->
## T-tampon dyal l-m3lumat (Message Broker)
<!-- Kafka ghadi tkun b7al chi "tampon" (boîte li t7ttha fih l-m3lumat), bash tfrq bayn l-jmii3 o t-t7awil dyal l-m3lumat. L-m3lumat ghadi t7ttha f-Kafka b-shakl mratb (distribué), o Zookeeper ghadi yshuf o ydir l-cluster dyal Kafka (y3ni yshuf kolchi khdam mzyan). Ghadi tsta3ml chi script shell smiyto "kafka-setup-k8s.sh" bash tdir l-topics (chi "dossiers" f-Kafka) dyal l-m3lumat f-Kubernetes (chi plateforme li tdir fih l-servers). -->
## T-t7awil f-l-waqt l-7aqiqi (Stream Processing)
<!-- Hna ghadi tsta3ml Spark Structured Streaming (partie mn Apache Spark) bash t7awwl l-m3lumat f-l-waqt l-7aqiqi. Spark ghadi yjma3 l-m3lumat mn Kafka, y7awwlha, ydir 3liha chi calculs (b7al l-moyenne, l-jamii3), o yb3athha l-database. -->
   ## L-mr7la l-ula (Transformation des Données Brutes): 
   <!-- Hna ghadi t7awwl l-m3lumat l-khama l-shakl mratb (structuré). Tnadfha (tnqss l-khawi), o tzid 3liha chi m3lumat bash tkun mzyan o tqdar tsta3mlha b-sah. -->
   ## L-mr7la t-tanya (Agrégations Temporelles): 
   <!-- Ghadi tdir chi calculs b7al l-moyenne dyal l-prix f-kol 5 secondes, wla tjm3 l-3amaliyat. Hadchi ghadi ydir l-m3lumat sri3a o jahza. Spark ghadi tsta3ml Spark-on-K8s-Operator bash tdir hada f-Kubernetes b-shakl automatique. -->
## T-7tizan dyal l-m3lumat (Stockage des Données)
<!-- L-m3lumat li 7wltieha ghadi t7ttha f-Cassandra (chi database sri3a). Ghadi tsta3ml chi fichier smiyto "cassandra-setup.cql" bash tdir l-keyspaces o l-tables (chi "dossiers" o "tables" f-database). Cassandra ghadi tkhddmha f-Kubernetes, o l-fichier hada ghadi ykhdm automatique bash tji l-database jahza. -->
## T-tshayf (Visualization)
<!-- B3d ma t7ttha l-m3lumat f-Cassandra, ghadi tsta3ml Grafana bash tshuf l-m3lumat f-tableaux de bord zwinin. Ghadi tsta3ml chi plugin smiyto "HadesArchitect-Cassandra" bash tqdar tshuf l-m3lumat mn Cassandra f-Grafana. L-gharad hiya tshuf l-indicateurs muhimma b-shakl graphique (b7al l-prix li tayr o ynzll). -->
## T-tanzim o l-infrastructure (Orchestration & Infrastructure)
<!-- Ghadi tsta3ml Kubernetes bash tdir kolchi (Kafka, Spark, Cassandra, Grafana) f-servers mratba, o tshuf kolchi khdam mzyan. Terraform ghadi tsta3mlha bash tdir l-clusters dyal Kubernetes o tshuf l-stockage o l-network. -->
## Nshufu l-picture o nqarnu m3a l-brief picture of architecture
<!-- L-picture li 3titini fih chi architecture li ktbtieha b-yddk, o ghadi nshufu chukayn t-tfaseel: -->

## Finnhub:               Hada kayna f-l-picture, o mratb m3a l-brief. Finnhub hiya l-source dyal l-m3lumat, o tsta3ml Websocket (ktbtie "Web S").
## Producer Kafka:        Hada tani kayna f-l-picture, o taba3 l-brief. L-producer hna hiya li tjma3 l-m3lumat mn Finnhub o tb3athha l-Kafka.
## Kafka-Setup-K8s.sh:    Hada tani mratb, ktbtie script shell li tdir l-topics f-Kafka f-Kubernetes.
## Spark:                 Hna ktbtie "Spark Structured Streaming" o "Spark-on-K8s/Helm", o hada mratb m3a l-brief. Spark hna hiya li t7awwl l-m3lumat f-l-waqt l-7aqiqi.
## L-mr7al dyal t-t7awil: Ktbtie "T1: RDD" (y3ni transformation l-ula), o "T2: Agrégations" (y3ni l-agrégations temporelles), o hada mratb m3a l-brief.
## Cassandra:             Hna ktbtie "Cassandra + CQL", o hada mratb m3a l-brief. Cassandra hiya l-database li t7ttha fih l-m3lumat.
## Grafana:               Hna tani mratb, ktbtie "Grafana" o "HadesArchitect Cassandra", o hada mratb m3a l-brief.
## Terraform:             Hna ktbtie "Terraform" f-l-picture, o hada mratb m3a l-brief, hiya li tdir l-infrastructure.


## Architecture de la solution
## Mermaid Code

graph TD
    A[Finnhub<br>Websocket] -->|Data Ingestion| B[Producer Kafka]
    B -->|Publishes Messages| C[Kafka<br>kafka-setup-k8s.sh<br>Zookeeper]
    C -->|Stream Processing| D[Spark Structured Streaming<br>Spark-on-K8s/Helm]
    D -->|T1: Transformation<br>Raw Data to Structured| E[T1: RDD]
    D -->|T2: Agrégations<br>Every 5 seconds| F[T2: Agrégations]
    E -->|Store Data| G[Cassandra<br>cassandra-setup.cql]
    F -->|Store Data| G
    G -->|Visualization| H[Grafana<br>HadesArchitect-Cassandra]
    I[Terraform<br>Kubernetes] -->|Orchestration| C
    I -->|Orchestration| D
    I -->|Orchestration| G
    I -->|Orchestration| H

## *************************************************************************************************************

spark_job.py:
Kayqra l-data mn Kafka topic financial_data.
Kayparse l-JSON data b-schema swiyya (symbol, price, volume, timestamp).
Kayb3t l-data l-Cassandra f-keyspace financial_data, table trades.
L-code mzyan o aligned m3a l-projet dyalek (transformation o stockage f-Cassandra).
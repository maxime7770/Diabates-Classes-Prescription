# Prescribing Diabetes Self-Management Classes

This project was developed as part of the Machine Learning Under an Optimization Lens class at MIT. It is a collaborative effort by team members [Maxime Wolf](https://www.linkedin.com/in/maxime-wolf/) and [Dilan SriDaran](https://www.linkedin.com/in/dilansridaran/)


## Introduction

### Background

Diabetes is a global health crisis, steadily rising in prevalence over recent decades. As of 2021, an
estimated 537 million people worldwide were grappling with diabetes, and projections indicate a
surge to 643 million by 2030.^1 This chronic metabolic disorder, characterized by elevated blood
glucose levels, poses substantial health risks and complications when not adequately managed,
including elevated risks of cardiovascular diseases, kidney failure, blindness, and neuropathy. This
imposes a significant burden on individuals, healthcare systems, and global economies.

Managing diabetes is complex, and achieving optimal glycemic control requires a comprehensive
approach beyond medical interventions. Lifestyle adjustments, dietary decisions, regular physical
activity, and medication adherence form integral components of effective self-management.
Nevertheless, a considerable segment of the diabetic population encounters challenges in adopting
and sustaining these changes. Identifying specific cohorts within this population most likely to benefit
from targeted interventions, like diabetes self-management classes, is pivotal for resource
optimization and overall improvement in outcomes.

Self-management empowers individuals with diabetes to play an active role in their care, creating a
sense of control and accountability. Educational programs geared towards enhancing self-
management skills give individuals knowledge and tools to make informed decisions about their
health, including effectively monitoring and regulating their blood glucose levels, mitigating the risk of
complications, and enhancing their overall well-being. Beyond immediate health benefits, successful
self-management has the potential to reduce healthcare costs associated with diabetes-related
complications, hospitalizations, and emergency care.

### Project Scope

This project aims to contribute to the advancement of diabetes care by identifying specific cohorts
of individuals who stand to gain the most from participation in diabetes self-management classes.
Using optimal policy trees, we analyze a diverse set of data including demographic information,
lifestyle factors, and social determinants of health. By identifying patterns and associations within this
data, our goal is to develop a predictive model that can stratify the diabetic population into cohorts
based on their likelihood of benefiting from self-management programs.


## Data

### Overview

The Behavioral Risk Factor Surveillance System (BRFSS) is a collaborative project between all of the
states in the United States and participating US territories and the Centers for Disease Control and
Prevention (CDC). The BRFSS is a system of ongoing health-related telephone surveys designed to
collect self-reported data on health-related risk behaviors, chronic health conditions, and use of preventive services from the noninstitutionalized adult population (18+ years) residing in the United
States. This project leverages the 2020 BRFSS Survey.

**Analysis Cohort**

While the survey spans 401,958 participants, we restrict our analysis to 13,047 individuals that self-
identified as having been diagnosed with diabetes. Of this cohort, 6,690 (51%) have previously taken
a course or class in self-managing their diabetes.

**Outcome**

We proxy health outcomes via two self-reported survey questions:

- “How many days during the past 30 days was your **physical health** not good?”
- “How many days during the past 30 days was your **mental health** not good?”

Notwithstanding clear data quality concerns surrounding self-reported metrics, we believe these two
features to be useful given that one of the primary aims of the self-management classes is to
empower and improve health perceptions of individuals with diabetes.

**Covariates**

The BRFSS dataset contains over 200 variables. To ensure interpretability of the final model, we
manually selected a subset of 47 of these variables based on a literature review of factors that are
important in diabetes prevalence, severity, and outcomes. These include, but are not limited to:

- Demographics: age, sex, race, and primary language
- Families and households: marital status, children, and safe households^2
- Socio-economics: education, employment, and income
- Lifestyles: exercise, sleep, alcohol consumption, and smoking (including e-cigarettes)
- Health conditions: 11 chronic condition flags and 4 activities of daily living flags
- Health access: health insurance coverage and residential rurality


### Data Cleaning

Given the data is collected through telephone surveys, missing information is a prevalent and critical
concern. In this data, there are two main forms through which missingness manifests:

1. **Question not asked:** Interviewers ask a series of questions that are guided by responses to
    prior questions. For example, if the respondent indicates that they have never smoked, the
    interviewer will not ask them a follow-up question about how many times they smoked over
    the past month.


For these cases, missing responses are assigned to the most appropriate value via
deterministic rules. In the example above, we set the number of times smoked over the past
month to be zero for an individual that has never smoked.

Unsafe households are those that have been identified as containing one or more individuals with drug or alcohol abuse problems, prior criminal
convictions, or severe depression.


2. **Question not answered:** For each question asked, typically response rates are in excess of
    90%, with a small proportion of individuals refusing to respond or being unsure.


For these cases, we implemented a data imputation framework. For variables with more than
25% missing values, we omitted the column. The remaining missing values were imputed using
a 𝑘-nearest neighbors approach.

Many variables in the data include impracticably granular responses, which raised the risk of
overfitting and non-interpretable models. Where relevant and appropriate, we grouped responses,
ensuring that the new groupings remained consistent and interpretable. For example, we grouped the
marital statuses “Divorced” and “Separated,” as the latter had a very low observation count.

We derive additional variables to better capture the risk profile of respondents. These include:

- Number of physical/mental conditions: Counting the number of chronic physical and mental
health conditions a patient reported. This better reflects the complexity of their physical and
mental care needs.
- Unsafe household indicator: Unsafe households were identified as containing one or more
individuals with drug or alcohol abuse problems, prior criminal convictions, or severe
depression. This may identify individuals with less stable support networks upon which to rely
for care, for whom access to self-management classes may be more beneficial.

## Approach

**Define Treatment**

The treatment is binary: whether or not an individual should take a class in self-management.

**Define Outcome**

The outcome is based on two self-reported metrics: “how many days during the past 30 days was
your physical health not good?” and “how many days during the past 30 days was your mental health
not good?”. We construct a weighted-combination of these variables:


**𝑦=𝜆(Number of Poor Physical Days)+( 1 −𝜆)(Number of Poor Mental Days)**

We provide a framework to implement and obtain results for various values of 𝜆. This allows medical
practitioners, who have greater domain expertise, to manage the relative importance placed on
physical and mental health outcomes.


**Estimate Training Rewards**

We use optimal policy trees (OPT) to determine the effectiveness of classes for individuals. OPTs
separate the tasks of estimating counterfactuals and learning the prescription policy. The first step
is to create the reward matrix, which represents the outcome for each sample in the data when
receiving and not receiving the class. We use a 50%/50% training/test split to save more data for
testing and ensure high-quality reward estimation for model evaluation. We use doubly-robust
reward estimation, testing various machine learning models (including XGBoost and Random Forest)
to estimate propensity scores and outcomes:

- **Propensity score estimation:** We use the area under the curve (AUC) criterion for evaluation.
    This is appropriate since the outcome is binary.
- **Outcome estimation:** We use the Tweedie metric for evaluation. This is because the
    outcome has a continuous distribution on positive values, except for a spike observed at
    exactly zero corresponding to “perfectly healthy” individuals. The Tweedie distribution
    accounts for this by modelling the number of unhealthy days as the sum of a Poisson number
    of independent Gamma variables.
  



<img width="857" alt="Screenshot 2024-02-28 at 11 35 57 AM" src="https://github.com/maxime7770/Diabetes-Classes-Prescription/assets/58089609/68e9338d-dd87-45bb-bcab-4ac1b25fe995">

Table 1: Evaluation metrics for different models (training data).



The evaluation metrics for our best models for various values of 𝜆 are summarized in Table 1, which
are XGBoost models in all instances. The metrics appear reasonable for our purpose, particularly given
that the doubly-robust estimation method is designed to deliver good results if either propensity
scores or outcomes are estimated well. We note that the Tweedie metric is weaker for lower values
of 𝜆 (more weight to mental health). This is intuitive, as mental health lacks the established biomarkers
of physical health outcomes, and is instead affected by intricate cognitive and emotional processes,
personal histories, and external stressors. Nevertheless, we choose to include mental health in our
analysis as we believe it is a crucial aspect of well-being that should be further studied.


**Learn Optimal Policy**

We learn an optimal policy tree that recommends whether an individual should take the class, based
on their characteristics, with the objective of minimizing the outcome variable.

**Estimate Testing Rewards**

<img width="848" alt="Screenshot 2024-02-28 at 11 36 23 AM" src="https://github.com/maxime7770/Diabetes-Classes-Prescription/assets/58089609/a047933c-d5c8-453a-a9d2-d36e197a7daf">

Table 2: Evaluation metrics for different models (test data).

For fair evaluation of the policy tree, we estimate a new set of rewards using only the test set and
evaluate the policy tree against these rewards. This is to avoid any information from the training set
leaking through to the out-of-sample evaluation. The scores are similar to those on the training set,
giving confidence that the estimated rewards will serve as a good and consistent basis for evaluation.

**Evaluate Policy**

We evaluate the quality of the policy tree prescriptions using the test set estimated rewards. We
compare average predicted outcomes under the prescribed treatments (“Prescribed”) to the average
outcomes actually observed (“Actual”) across the test set.

Table 3 illustrates outcomes, showing a material improvement under the prescribed policies. This is
most pronounced for mental health outcomes. Despite the prior observation of the models being less
predictive for this outcome, this remains a notable finding as it supports the recent focus on
emphasizing resilience and coping strategies in self-management curricula.

<img width="853" alt="Screenshot 2024-02-28 at 11 36 50 AM" src="https://github.com/maxime7770/Diabetes-Classes-Prescription/assets/58089609/4713aee3-f824-42ea-923f-a89041b483e7">

Table 3: Comparison of prescribed and actual outcomes.

## Insights

In this section, we explore the optimal policy tree for three distinct values of 𝜆, specifically focusing
on cohorts identified to most strongly benefit from receiving self-management classes.

### Mental Health Model (𝜆=0)


- Patients without concentration issues (9.3% improvement): Generally, patients without
concentration issues appear likely to benefit from classes, as they likely have greater potential
to absorb and retain the information presented in the classes.
- Patients with depression and concentration and sleep issues, but have completed high
school (39.5% improvement): Individuals struggling with cognitive function, who have
completed high school, may still have the ability to comprehend and apply materials learned.
These classes can be particularly helpful in providing coping strategies to those struggling
with depression and can offer strategies to improve sleep hygiene, which is known to affect
blood glucose levels and insulin sensitivity.
- Patients with concentration issues, living in households free of alcohol abuse (110.6%
improvement): Individuals in more stable homes may have a better environment to focus on
and prioritize their own well-being, rather than worrying or taking care of those around them.


<img width="1250" alt="Screenshot 2024-02-28 at 11 39 06 AM" src="https://github.com/maxime7770/Diabetes-Classes-Prescription/assets/58089609/32df7b0d-467d-4d98-b070-8aefc008dd12">

Figure 1: Optimal policy tree for mental health outcomes (𝜆=0)


### Physical Health Model (𝜆=1)

<img width="667" alt="Screenshot 2024-02-28 at 11 39 22 AM" src="https://github.com/maxime7770/Diabetes-Classes-Prescription/assets/58089609/1cce583f-a4a5-4217-8cee-42732ef5a5e8">

Figure 2: Optimal policy tree for physical health outcomes (𝜆=1)


- Young females with multiple physical conditions (23.5% improvement): Women with
multiple physical conditions are likely to have complex care needs and are likely to benefit
strongly from being taught tailored strategies to manage their health.
- Young males (11.6% improvement): There is a tendency among young individuals, particularly
males, to exhibit a higher level of self-assurance, often leading them to believe they are at
lower risk and do not need to invest time in educating themselves about diabetes. Classes
may be effective for this cohort to promote better diabetes control and lifestyle adjustments.
- Older individuals with no cancer or chronic obstructive pulmonary disease (COPD) (56%
improvement): Diabetes classes appear most effective at older ages, as individuals may have
more complex health needs, are more likely to live alone or without care givers, and may be
less familiar with using the internet to obtain information. Individuals with cancer and COPD
may have materially complex needs that are better managed by medical practitioners.


### Blended Model (𝜆=0.6)


<img width="668" alt="Screenshot 2024-02-28 at 11 40 44 AM" src="https://github.com/maxime7770/Diabetes-Classes-Prescription/assets/58089609/3c76b60e-770c-49b4-807f-46a1d75075bf">

Figure 3: Optimal policy tree for blended health outcomes (𝜆=0.6)


- Young people with sleep issues and have children (51% improvement): This group is likely
juggling the challenges of parenting with their own sleep-related difficulties, impacting their
ability to manage diabetes effectively, and would benefit from learning appropriate strategies.
- Older individuals without COPD conditions (24% improvement): As discussed in the
“Physical Health” model, older individuals without COPD will likely benefit from classes.


## Conclusion and Next Steps

This project has shown the potential to use policy trees to identify cohorts that are likely to have the
greatest benefit from attending diabetes self-management classes. This has the potential to inform
recommendations from doctors, the design of government policies or subsidies, and ultimately
contribute to improved health outcomes for individuals living with diabetes. There are avenues to
enhance the model further, including applying the model to non-self-reported data (to provide more
objective measures) and expanding the scope of features considered. For example, the BRFSS data
does not distinguish Type I and Type II patients, for whom we believe outcomes may be considerably
different.

Before refining, enhancing, or deploying the model, we believe it crucial to validate them with medical
practitioners to ensure their accuracy, reliability, and practical relevance within the healthcare
context. Medical practitioners bring invaluable real-world clinical expertise and experience that can
uncover nuances and intricacies not captured by the data alone. This can help identify potential
biases, refine the model's features, and enhance its clinical interpretability. Moreover, involving domain
experts in the validation process allows us to align our prescriptions with current medical knowledge,
established standards of care, and clinical guidelines.

To support potential discussions with medical experts, we have developed an interactive user
interface (see below). The tool allows users to select various values of 𝜆, and to observe the policy
tree and predicted outcomes (and improvements), which can be discussed, critiqued, and validated.
The tool also provides functionality to input specific patient characteristics and output the
prescribed policy, which may be useful should the model be deployed in a clinical setting.


## User Interface

<img width="1022" alt="Screenshot 2024-02-28 at 11 42 05 AM" src="https://github.com/maxime7770/Diabetes-Classes-Prescription/assets/58089609/f052b149-0dca-4637-9ffc-1673acc5e8ad">


<img width="1181" alt="Screenshot 2024-02-28 at 11 42 17 AM" src="https://github.com/maxime7770/Diabetes-Classes-Prescription/assets/58089609/635d106c-8959-4a74-9b48-f928de9292b1">

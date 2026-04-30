# Artificial Bestiary — rich analysis summary

## Dataset

- Rows: 1,800
- Usable responses: 1,800
- Errors: 0
- Empty non-error responses: 0
- Conditions observed: 10
- Words observed: 9

## Headline baseline comparisons

- Presupposed prompts averaged 132.2 words vs 79.5 for neutral (Welch t=38.01, p=7.65e-216).
- Substantive-generation heuristic: 37.2% for presupposed prompts vs 0.6% for neutral (Fisher exact OR=106.13, p=1.14e-32).
- Epistemic-caveat rate: 67.2% for presupposed prompts vs 99.4% for neutral.

## Condition-level descriptive summary

| condition        |   n |   word_count_mean |   word_count_sd |   epistemic_caveat_rate |   refusal_or_noninvent_rate |   creative_frame_rate |   high_specificity_rate |   substantive_generation_rate |   category_aligned_rate |   specific_terms_total_mean |
|:-----------------|----:|------------------:|----------------:|------------------------:|----------------------------:|----------------------:|------------------------:|------------------------------:|------------------------:|----------------------------:|
| imaginary_animal | 180 |           205.611 |          19.44  |                   0.028 |                       0.017 |                 0.506 |                   0.906 |                         0.967 |                   0.994 |                       8.894 |
| imaginary_idea   | 180 |           159.894 |          32.106 |                   0.456 |                       0.033 |                 0.978 |                   0.333 |                         0.728 |                   0.561 |                       4.644 |
| imaginary_object | 180 |           191.522 |          41.102 |                   0.139 |                       0.05  |                 0.811 |                   0.706 |                         0.806 |                   0.894 |                       7.172 |
| neutral          | 180 |            79.517 |           9.666 |                   0.994 |                       0     |                 0.672 |                   0.006 |                         0.006 |                 nan     |                       2.233 |
| real_animal      | 180 |            89.511 |          10.509 |                   0.839 |                       0.217 |                 0.15  |                   0.028 |                         0.028 |                   0.967 |                       3.839 |
| real_idea        | 180 |            94.417 |          13.137 |                   0.95  |                       0.367 |                 0.067 |                   0.028 |                         0.033 |                   0.356 |                       2.406 |
| real_object      | 180 |            86.389 |          11.394 |                   0.772 |                       0.189 |                 0.072 |                   0.006 |                         0.006 |                   0.994 |                       2.394 |
| type_of_animal   | 180 |           118.922 |          19.6   |                   0.972 |                       0.283 |                 0.994 |                   0.278 |                         0.289 |                   0.956 |                       4.644 |
| type_of_idea     | 180 |           132.867 |          19.466 |                   1     |                       0.206 |                 0.972 |                   0.072 |                         0.394 |                   0.928 |                       3.011 |
| type_of_object   | 180 |           110.422 |          21.773 |                   0.889 |                       0.117 |                 0.983 |                   0.028 |                         0.1   |                   0.722 |                       2.117 |

## Largest word-count increases over neutral

| condition        |   condition_mean |   baseline_mean |   difference |   effect_size |   p_holm |
|:-----------------|-----------------:|----------------:|-------------:|--------------:|---------:|
| imaginary_animal |          205.611 |          79.517 |      126.094 |         8.214 |        0 |
| imaginary_object |          191.522 |          79.517 |      112.006 |         3.751 |        0 |
| imaginary_idea   |          159.894 |          79.517 |       80.378 |         3.39  |        0 |
| type_of_idea     |          132.867 |          79.517 |       53.35  |         3.472 |        0 |
| type_of_animal   |          118.922 |          79.517 |       39.406 |         2.55  |        0 |
| type_of_object   |          110.422 |          79.517 |       30.906 |         1.835 |        0 |
| real_idea        |           94.417 |          79.517 |       14.9   |         1.292 |        0 |
| real_animal      |           89.511 |          79.517 |        9.994 |         0.99  |        0 |
| real_object      |           86.389 |          79.517 |        6.872 |         0.65  |        0 |

## Largest substantive-generation increases over neutral

| condition        |   condition_mean |   baseline_mean |   difference |   effect_size |   p_holm |
|:-----------------|-----------------:|----------------:|-------------:|--------------:|---------:|
| imaginary_animal |            0.967 |           0.006 |        0.961 |      5191     |    0     |
| imaginary_object |            0.806 |           0.006 |        0.8   |       741.571 |    0     |
| imaginary_idea   |            0.728 |           0.006 |        0.722 |       478.551 |    0     |
| type_of_idea     |            0.394 |           0.006 |        0.389 |       116.596 |    0     |
| type_of_animal   |            0.289 |           0.006 |        0.283 |        72.719 |    0     |
| type_of_object   |            0.1   |           0.006 |        0.094 |        19.889 |    0     |
| real_idea        |            0.033 |           0.006 |        0.028 |         6.172 |    0.364 |
| real_animal      |            0.028 |           0.006 |        0.022 |         5.114 |    0.43  |
| real_object      |            0.006 |           0.006 |        0     |         1     |    1     |
## Coding notes

The added columns are rule-based heuristics, not final human labels.

- `epistemic_caveat`: phrases like "doesn't appear", "I don't recognize", or "not in my knowledge".
- `refusal_or_noninvent`: explicit language about not inventing or not providing a factual description.
- `creative_frame`: explicit fictional / imaginary / made-up / speculative framing.
- `high_specificity`: at least 6 animal/object/idea/domain-term hits.
- `substantive_generation`: high specificity, or a long response with multiple domain-marker classes.
- `category_aligned`: whether the lexicon-inferred dominant category matches the prompted category.
- `cautious_nonanswer`: caveat + context/help request + no substantive-generation flag.
- `caveated_generation`: caveat + substantive-generation flag.

Treat `substantive_generation` as a confabulation-adjacent screening measure rather than a
definitive hallucination label. It is useful for finding responses that probably warrant
hand coding.

## Plots written

- `plot_word_count_by_condition.png`
- `plot_feature_rates_by_condition.png`
- `plot_specific_terms_by_condition.png`

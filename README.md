# Measuring Pointwise V-Usable Information In-context-ly

> **Abstract:** In-context learning (ICL) is a new learning paradigm that has gained popularity along with the development of large language models. In this work, we adapt a recently proposed hardness metric, pointwise V-usable information (PVI), to an in-context version (in-context PVI). Compared to the original PVI, in-context PVI is more efficient in that it requires only a few exemplars and does not require fine-tuning. We conducted a comprehensive empirical analysis to evaluate the reliability of in-context PVI. Our findings indicate that in-context PVI estimates exhibit similar characteristics to the original PVI. Specific to the in-context setting, we show that in-context PVI estimates remain consistent across different exemplar selections and numbers of shots. The variance of in-context PVI estimates across different exemplar selections is insignificant, which suggests that in-context PVI estimates are stable. Furthermore, we demonstrate how in-context PVI can be employed to identify challenging instances. Our work highlights the potential of in-context PVI and provides new insights into the capabilities of ICL.

Contact person: Sheng Lu

https://www.ukp.tu-darmstadt.de/

https://www.tu-darmstadt.de/

## in-context PVI
See [in_context_pvi.ipynb](https://github.com/UKPLab/in-context-pvi/blob/main/in_context_pvi.ipynb) for the calculation of in-context PVI.

## evaluation scores
See [results.csv](https://github.com/boblus/in-context-pvi/blob/main/results.csv) for the configurations and evaluation scores of our experiments.

## disclaimer
This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication.

## citation
Please use the following citation:

```
@inproceedings{lu-etal-2023-measuring,
    title = "Measuring Pointwise $\mathcal{V}$-Usable Information In-Context-ly",
    author = "Lu, Sheng  and
      Chen, Shan  and
      Li, Yingya  and
      Bitterman, Danielle  and
      Savova, Guergana  and
      Gurevych, Iryna",
    editor = "Bouamor, Houda  and
      Pino, Juan  and
      Bali, Kalika",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2023",
    month = dec,
    year = "2023",
    address = "Singapore",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.findings-emnlp.1054",
    pages = "15739--15756",
    abstract = "In-context learning (ICL) is a new learning paradigm that has gained popularity along with the development of large language models. In this work, we adapt a recently proposed hardness metric, pointwise $\mathcal{V}$-usable information (PVI), to an in-context version (in-context PVI). Compared to the original PVI, in-context PVI is more efficient in that it requires only a few exemplars and does not require fine-tuning. We conducted a comprehensive empirical analysis to evaluate the reliability of in-context PVI. Our findings indicate that in-context PVI estimates exhibit similar characteristics to the original PVI. Specific to the in-context setting, we show that in-context PVI estimates remain consistent across different exemplar selections and numbers of shots. The variance of in-context PVI estimates across different exemplar selections is insignificant, which suggests that in-context PVI estimates are stable. Furthermore, we demonstrate how in-context PVI can be employed to identify challenging instances. Our work highlights the potential of in-context PVI and provides new insights into the capabilities of ICL.",
}
```

# Measuring Pointwise V-Usable Information In-context-ly

> **Abstract:** In-context learning (ICL) is a new learning paradigm that has gained popularity along with the development of large language models. In this work, we adapt a recently proposed hardness metric, pointwise V-usable information (PVI), to an in-context version (in-context PVI). Compared to the original PVI, in-context PVI is more efficient in that it requires only a few exemplars and does not require fine-tuning. We conducted a comprehensive empirical analysis to evaluate the reliability of in-context PVI. Our findings indicate that in-context PVI estimates exhibit similar characteristics to the original PVI. Specific to the in-context setting, we show that in-context PVI estimates remain consistent across different exemplar selections and numbers of shots. The variance of in-context PVI estimates across different exemplar selections is insignificant, which suggests that in-context PVI estimates are stable. Furthermore, we demonstrate how in-context PVI can be employed to identify challenging instances. Our work highlights the potential of in-context PVI and provides new insights into the capabilities of ICL.

Contact person: Sheng Lu

https://www.ukp.tu-darmstadt.de/

https://www.tu-darmstadt.de/

## evaluation scores
See [results](https://github.com/boblus/in-context-pvi/blob/main/results.csv) for the configurations and evaluation scores of our experiments.

## citation
Please use the following citation:

```
@misc{lu2023measuring,
      title={Measuring Pointwise $\mathcal{V}$-Usable Information In-Context-ly}, 
      author={Sheng Lu and Shan Chen and Yingya Li and Danielle Bitterman and Guergana Savova and Iryna Gurevych},
      year={2023},
      eprint={2310.12300},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

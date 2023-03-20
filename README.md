# NaturalMSEQueries: A natural way to query Materials Science Engineering data experiments

## Abstract
Materials science experiments involve complex data that are often very heterogeneous and challenging to reproduce. This was observed, for example, in a previous study on harnessing lightweight design potentials via the Materials Data Space [3] for which the data from materials sciences engineering experiments were generated using linked open data principles [1,2], e.g., Resource Description Framework (RDF) as the standard model for data interchange on the Web. However, detailed knowledge of formulating questions in the query language SPARQL is necessary to query the data. A lack of knowledge in SPARQL to query data was observed by domain experts in materials science.
With this work, we aim to develop NaturalMSEQueries an approach for the material science domain expert where instead of SPARQL queries, the user can develop expressions in natural language, e.g., English, to query the data. This will significantly improve the usability of Semantic Web approaches in materials science and lower the adoption threshold of the methods for the domain experts. We plan to evaluate our approach, with varying amounts of data, from different sources. Furthermore, we want to compare with synthetic data to assess the quality of the implementation of our approach. 

### References
```
[1] T Berners-Lee, J Hendler, O Lassila - Scientific American, 2001, 284, 34–43.
[2] RDF specification. 2023. available at: https://www.w3.org/RDF/
[3] Huschka M, Dlugosch M, Friedmann V, Trelles EG, Hoschke K, Klotz UE, Patil S, Preußner J, Schweizer C, Tiberto D. The “AluTrace” Use Case: Harnessing Lightweight Design Potentials via the Materials Data Space®.
```

# KnowledgeUI
Flask App Frontend Application Showing The Benefits Of Rich Semantic Material Science Data And Exemplar Usage.
![workflow](https://user-images.githubusercontent.com/9248325/215797610-0e838dca-e8ed-4c2a-8ac7-af8ffffec162.png)

# how to use
The code is supposed to run as docker-compose stack

## As a developer
```bash
git clone https://github.com/Mat-O-Lab/KnowledgeUI
```
```bash
cd KnowledgeUI
```
```bash
pip install -r requirements.txt
```
```bash
python app.py
```
Your app will be available at http://localhost:5000

## docker-compose
Clone the repo with 
```bash
git clone https://github.com/Mat-O-Lab/KnowledgeUI
```
cd into the cloned folder
```bash
cd KnowledgeUI
```
Build and start the container.
```bash
docker-compose up
```

# Cite us:
```
@software{andre_valdestilhas_2023_7744532,
  author       = {Andre Valdestilhas and
                  Thomas Hanke},
  title        = {{NaturalMSEQueries - A natural way to query 
                   Material Sciences Engineering data experiments}},
  month        = mar,
  year         = 2023,
  publisher    = {Zenodo},
  version      = {1.0},
  doi          = {10.5281/zenodo.7744532},
  url          = {https://doi.org/10.5281/zenodo.7744532}
}
```

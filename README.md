# CHIIR 2019 Code and Documents
Herein are the code and documents for reproducibility purposes of our publication.  Web pages as displayed to users can be found here: 'static/webpage_img'.   Web page meta data, including 3rd party tracker data, can be found here: 'resources/data/annotations/json'.   Anonomyized participant data can be found in 'CHIIR_2019_data_anonymized.xlsx'.


# Citing work
Please use information in the following bibtex entry for citation, and be sure to cite other relevant works contained within (e.g. Pogacar et al. 2017, White et al. 2014, etc.).

```
@inproceedings{Zimmerman2019Privacy,
 author = {Zimmerman, S. and Thorpe, A. and Fox, C. and Kruschwitz, U.},
 title = {Privacy Nudging in Search: Investigating Potential Impacts},
 booktitle = {Proceedings of the 2019 Conference on Human Information Interaction and Retrieval},
 series = {CHIIR '19},
 year = {2019},
 location = {Glasgow, Scotland UK},
 pages = {283--287}
} 
```

# Setup
Install requirements on python 3.6

# Usage
```
python main.py
```

1. Open a browser an navigate to http://localhost:5000/login
2. Enter the participant ID   (T0001 and T0002 are included, use 'resources/scripts/setup/create_participants_from_master_list.py' to add participants)
3. Experiment can then be run for participant ID.  Tested for 3 concurrent participants.
4. Once all participants are run you can run a report to combine all experiment data into a CSV 'src/analysis/report/compare_interface_decision.py'



# License
MIT License

Copyright (c) 2018 Steven E. Zimmerman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

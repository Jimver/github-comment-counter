# GitHub comment counter

This repo contains a small script that counts the comments on a repository on GitHub. 
It can count the amount of comments in issues, PRs or both combined. It also has the ability
to filter the issues/PRs based on a label. Multiple labels can be given to give an overview of 
comment counts across different labels.


Example output in csv (first 6 rows):
```csv
username,component: numpy.core,component: numpy.fft
seberg,222,23
mattip,148,14
charris,121,118
eric-wieser,114,10
rgommers,50,38
mhvk,49,14
```
 
And a more readable version in markdown for this README.

| username    | component: numpy.core | component: numpy.fft |
|-------------|-----------------------|----------------------|
| seberg      | 222                   | 23                   |
| mattip      | 148                   | 14                   |
| charris     | 121                   | 118                  |
| eric-wieser | 114                   | 10                   |
| rgommers    | 50                    | 38                   |
| mhvk        | 49                    | 14                   |
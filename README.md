# GitHub comment counter

This repo contains a small script that counts the comments on a repository on GitHub. 
It can count the amount of comments in issues, PRs or both combined. It also has the ability
to filter the issues/PRs based on a label. Multiple labels can be given to give an overview of 
comment counts across different labels.

## Usage

First clone or download this repository locally.

Go to the root of the repository and install required packages using `pip`:

`pip install -r requirements.txt`

Then run the program by invoking it using:

`github-comment-counter.py [OPTIONS]`

The [OPTIONS] contain the CLI arguments:
- `--repo_name REPO_NAME` The repository name, for example `numpy`.
- `--repo_owner` The owner of the repository, in the case of NumPy this is also `numpy`.
- `--label` The label of the issues / PRs to filter on. To analyse multiple labels you can put more of them after each other. (See example below) 
- `--issues/--no-issues` flag that controls whether to take issues into account.
- `--pull_requests/--no-pull_requests` flag that controls whether to take PRs into account.
- `--help` for instructions.

Note that you should put strings with spaces between double quotes (") for proper argument parsing.

Example command:
```
github-comment-counter.py --repo_name numpy --repo_owner numpy -label "component: numpy.core" -label "component: numpy.fft" -issues -pull_requests
```

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
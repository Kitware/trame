## Contributing to Trame

First off, thank you for considering contributing to Trame. It’s people like you that make Trame such a great tool.

## Support
For help and support in using Trame, please visit our forum [here](https://discourse.paraview.org)

## Issues, bugs, and feature requests
Open a new issues [here](https://github.com/Kitware/trame/issues/new/choose) to bring something to our attention.

## Development
We recommend this workflow when working on Trame

1. Fork and clone this repository (instructions [here](https://help.github.com/articles/fork-a-repo/))

2. Create a python virtual environment for development, eg
```sh
cd trame
python3 -m venv .venv
source .venv/bin/activate
```

3. `pip` install Trame in "editable mode." This will let python respond to any changes you make to Trame itself.
```sh
pip install -e .
```

4. Create a feature branch and start hacking.
```sh
git checkout -b new_feature
edit file1 file2 file3
git add file1 file2 file3
```

5. Use Commitizen to create commits or follow [Angular commit message conventions](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format).

To run commitizen, you will need to install the project tools.
```sh
npm install 
```
Then for each commit you can run this.
```sh
npm run commit
```

6. Push commits in your feature branch to your fork in GitHub:

```sh
$ git push origin new_feature
```

7. Visit your fork in Github, browse to the "**Pull Requests**" link on the left, and use the "**New Pull Request**" button in the upper right to create a Pull Request.
For more information see: 
[Create a Pull Request](https://help.github.com/articles/creating-a-pull-request/)

8. We will review your pull request. Be sure to include a clear and concise description of what the problem was and how this pull request solves it.

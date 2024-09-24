# CHANGELOG

## v0.4.0 (2024-09-24)

### Feature

* feat: add plotting function to call dlc `PlottingResults` on PoseEstimation results ([`d05c664`](https://github.com/datajoint/element-deeplabcut/commit/d05c66417e59e483bbcc0f6e05604f12c5580f7e))

### Fix

* fix(dlc_plots): bugfix import errors ([`144c34a`](https://github.com/datajoint/element-deeplabcut/commit/144c34a84977c710b572eec79b4de24a608f0708))

* fix(pose_estimation): Save config to outbox as dj_dlc_config ([`f69c46a`](https://github.com/datajoint/element-deeplabcut/commit/f69c46a7ff4d9ec62bdc57ce99315cfc241a8e59))

### Unknown

* Merge pull request #131 from datajoint/semantic-release-with-github-app

Semantic release with GitHub app ([`088a8ab`](https://github.com/datajoint/element-deeplabcut/commit/088a8ab2f637c083257e48313d0b30993bee37ca))

* Update test.yaml ([`3eec2bf`](https://github.com/datajoint/element-deeplabcut/commit/3eec2bf87797ff5c993778f839bb78a0e3c6abe4))

* Update semantic-release-caller.yml ([`61b3f65`](https://github.com/datajoint/element-deeplabcut/commit/61b3f659fcde6520221e55ded3ad911b4497acd4))

* Merge pull request #129 from ttngu207/main ([`f7cac84`](https://github.com/datajoint/element-deeplabcut/commit/f7cac84e2812c93401d35601f7a5d61d3068f414))

* Merge pull request #126 from ttngu207/main

add plotting function to call dlc PlottingResults on PoseEstimation results ([`af4ce80`](https://github.com/datajoint/element-deeplabcut/commit/af4ce80acf21559b6f7c5eb53452432c4619135c))

* bump version ([`ddd5c16`](https://github.com/datajoint/element-deeplabcut/commit/ddd5c16bb5716ef3a4f7fc343af1d8c245eb6b41))

* Merge pull request #124 from ttngu207/main

fix(pose_estimation): Save config to outbox as dj_dlc_config ([`a1073bb`](https://github.com/datajoint/element-deeplabcut/commit/a1073bbd22da39daf2e94840c3a4d9185f200bd0))

## v0.3.1 (2024-09-16)

### Chore

* chore: explicit &amp; consistent `config_filename ` ([`129f661`](https://github.com/datajoint/element-deeplabcut/commit/129f661b8d905320f06bfd5d46b09757c97cd387))

* chore: rename `dlc_model` to avoid easy naming collision ([`bdf0ae2`](https://github.com/datajoint/element-deeplabcut/commit/bdf0ae250a3bf2f17a55dc3d2d364e94a92c9584))

* chore: improve imports, avoid circular dependencies ([`bf02c7c`](https://github.com/datajoint/element-deeplabcut/commit/bf02c7c2f9e0ffe5c446032c5774d7d181c41281))

* chore: code cleanup ([`6c10ac7`](https://github.com/datajoint/element-deeplabcut/commit/6c10ac7a376b602bacf8dc5805825ebbefc8af3d))

* chore: black formatting + improve Windows/Linux path robustness ([`c13611d`](https://github.com/datajoint/element-deeplabcut/commit/c13611d3033d032ecfb927c09605bc91050fecac))

* chore(tests): set tear down to True ([`5897edd`](https://github.com/datajoint/element-deeplabcut/commit/5897edd0eeb4062aa2ab0f216894f4bc3b0b077f))

### Documentation

* docs: :bug: update mkdocs.yaml ([`c228d8e`](https://github.com/datajoint/element-deeplabcut/commit/c228d8e3905b87f9b36d09f12f4ec16b51fb214a))

### Feature

* feat: better handling for &#34;cropping&#34; input ([`fd6ba27`](https://github.com/datajoint/element-deeplabcut/commit/fd6ba277204fe2f3a3f9f5d092f38e319f2ee628))

* feat(pose_estimation): use `memoized_results` ([`fe8224b`](https://github.com/datajoint/element-deeplabcut/commit/fe8224b677b69028700f2ed4f06f6ec62c92d60e))

* feat(tests): add pytest ([`9133925`](https://github.com/datajoint/element-deeplabcut/commit/91339258760d7d94488df13ec513f8872458f910))

### Fix

* fix: remove prototyping code ([`52175f4`](https://github.com/datajoint/element-deeplabcut/commit/52175f4704bd0b93e541e9afd599fef1450bdff1))

* fix: minor import bug ([`c061e9a`](https://github.com/datajoint/element-deeplabcut/commit/c061e9af342c30894345eccc809c40ce51082147))

* fix: directly implement logic of `do_pose_estimation` in the `make` ([`c7aba7d`](https://github.com/datajoint/element-deeplabcut/commit/c7aba7d1b16fe0a906418b95cab373ffbafe5960))

* fix: remove &#34;print&#34; statement ([`0044441`](https://github.com/datajoint/element-deeplabcut/commit/00444414957a52cc5384c97f7367b2dab91b3eb3))

* fix(tests): clean up notebook ([`47bbbbc`](https://github.com/datajoint/element-deeplabcut/commit/47bbbbc894c74e08c9abb0544cd594664cccc9cf))

* fix(tests): minor bugfix in tests ([`9151e69`](https://github.com/datajoint/element-deeplabcut/commit/9151e6953c08bc8071bbb0fe5ef7673fa6724c0f))

### Style

* style: black formatting ([`61ee5fa`](https://github.com/datajoint/element-deeplabcut/commit/61ee5fad21ce833ee69191b65e8c9484909b0b45))

### Unknown

* Merge pull request #121 from ttngu207/main

add new table `LabeledVideo` to generate/store labeled video data after PoseEstimation ([`117694e`](https://github.com/datajoint/element-deeplabcut/commit/117694e698f20f6d9d363be03a416f641cc78c7c))

* Revert &#34;Update tutorial_pipeline.py&#34;

This reverts commit 079641d45835507fcda1bf0822a4f8c025dde337. ([`8fff7b0`](https://github.com/datajoint/element-deeplabcut/commit/8fff7b0b3936731129b00612fa9f57f8e5bc63f2))

* Update tutorial_pipeline.py ([`079641d`](https://github.com/datajoint/element-deeplabcut/commit/079641d45835507fcda1bf0822a4f8c025dde337))

* update: version, changelog ([`783985c`](https://github.com/datajoint/element-deeplabcut/commit/783985cd78ba230eb58ab2dd80bb9b245541670e))

* Merge remote-tracking branch &#39;upstream/main&#39; ([`70630b0`](https://github.com/datajoint/element-deeplabcut/commit/70630b025229e773b9df675826df21c49d6c6189))

* Merge pull request #120 from ttngu207/main

feat(pose_estimation): use `memoized_results` ([`2833f15`](https://github.com/datajoint/element-deeplabcut/commit/2833f159ecf691868a227ad6e200b6d5830033b0))

* Merge pull request #119 from ttngu207/main

chore: improve imports, avoid circular dependencies ([`34a6edb`](https://github.com/datajoint/element-deeplabcut/commit/34a6edb22510d52f53085325962b5b6dcca37acd))

* Merge branch &#39;dev_create_labeled_video&#39; into iub-lulab ([`d2ed00a`](https://github.com/datajoint/element-deeplabcut/commit/d2ed00a25d9e7f5baf7f50ac4aeb5636d3341a85))

* update: bump version ([`c2eb090`](https://github.com/datajoint/element-deeplabcut/commit/c2eb09029ca4cfd1f182f7472799170c09b72d2e))

* Merge branch &#39;main&#39; of https://github.com/ttngu207/element-deeplabcut ([`d1dcc46`](https://github.com/datajoint/element-deeplabcut/commit/d1dcc46aa3f3fbfbc093332ba594a8f38882e954))

* Merge pull request #118 from MilagrosMarin/main ([`25405b4`](https://github.com/datajoint/element-deeplabcut/commit/25405b48a8c9edb98c79f66d4c5abbf607c02247))

* Merge pull request #116 from datajoint/MilagrosMarin-patch-1

Create semantic-release-caller.yml ([`c2ea14f`](https://github.com/datajoint/element-deeplabcut/commit/c2ea14ff08ec49fb7b217db4d5b09c06111f219e))

* Create semantic-release-caller.yml ([`e9f96d7`](https://github.com/datajoint/element-deeplabcut/commit/e9f96d70347346fcdb2607ca3e56a4750579ebc0))

* Merge pull request #115 from datajoint/MilagrosMarin-patch-1

Update devcontainer-build-publish-caller.yml ([`4a954bf`](https://github.com/datajoint/element-deeplabcut/commit/4a954bf9df71e7a091c9a01188c8607044769be5))

* Update devcontainer-build-publish-caller.yml ([`9af7d83`](https://github.com/datajoint/element-deeplabcut/commit/9af7d837e999b6339c143828a0b5e1c6789a224c))

* Merge pull request #114 from datajoint/MilagrosMarin-patch-2

Create mkdocs-release-caller.yml ([`b7f0842`](https://github.com/datajoint/element-deeplabcut/commit/b7f0842cdcd119a9bffc3d8edd0892a61a1db01e))

* Create mkdocs-release-caller.yml ([`5e219cf`](https://github.com/datajoint/element-deeplabcut/commit/5e219cf6c5c47fe6696d7ead48e2b5e80409a3bd))

* Merge pull request #113 from datajoint/MilagrosMarin-patch-1

Update devcontainer-build-publish-caller.yml ([`dbec5b2`](https://github.com/datajoint/element-deeplabcut/commit/dbec5b26544aa2efaf9d70ba63e827601d7a0a09))

* Update devcontainer-build-publish-caller.yml ([`20b8753`](https://github.com/datajoint/element-deeplabcut/commit/20b87536043d67d0e27d3ae904fb4e9b3379b975))

* Merge pull request #112 from datajoint/MilagrosMarin-patch-1

Create devcontainer-build-publish-caller.yml ([`84db8ad`](https://github.com/datajoint/element-deeplabcut/commit/84db8ad563054271f29b28af62b511ab9ddde31e))

* Create devcontainer-build-publish-caller.yml ([`708d071`](https://github.com/datajoint/element-deeplabcut/commit/708d071961aabc74f88bda0546bcb6b99f4b8be1))

* Merge pull request #111 from MilagrosMarin/main

Fix: style tests ([`7f2dd68`](https://github.com/datajoint/element-deeplabcut/commit/7f2dd68c91aea149e05206aafa31b3d477977efd))

* update version and changelog ([`2304d09`](https://github.com/datajoint/element-deeplabcut/commit/2304d09e445a45aad7642b9cbf7b3d55abe3c501))

* black formatting ([`284abf6`](https://github.com/datajoint/element-deeplabcut/commit/284abf62e2ed2c11c98ed74d434746c14447ad72))

* Merge branch &#39;datajoint:main&#39; into main ([`3b68844`](https://github.com/datajoint/element-deeplabcut/commit/3b688442bc66c4cd37cc7e02dc7bc2b2c40d19f6))

* Merge pull request #110 from datajoint/staging

Bugfix - store `snapshotindex` for the latest snapshot instead of the filename ([`1cf8347`](https://github.com/datajoint/element-deeplabcut/commit/1cf8347ea023bebd2c375f6ff725f7ced7d8ff8c))

* Merge remote-tracking branch &#39;refs/remotes/origin/main&#39; ([`9cf3cef`](https://github.com/datajoint/element-deeplabcut/commit/9cf3cef90729eee69241bf0927d7563fd049ed85))

* Merge pull request #108 from ttngu207/main

style: black formatting ([`e6944a9`](https://github.com/datajoint/element-deeplabcut/commit/e6944a99327074283bdd0f7c3e5eebeb9ed57c50))

* black formatting ([`a31e56f`](https://github.com/datajoint/element-deeplabcut/commit/a31e56f9469aabedd065acb613660495a8855a18))

* Merge remote-tracking branch &#39;upstream/staging&#39; ([`1941bdb`](https://github.com/datajoint/element-deeplabcut/commit/1941bdbed1a1db62b5a44610bcc702233e103cda))

* Merge pull request #105 from ttngu207/dev_test_dlc_training

Code cleanup + minor bugfix in cross platform paths formatting ([`7949f61`](https://github.com/datajoint/element-deeplabcut/commit/7949f617c7608ed958757fb56a5497a56f587b95))

* Merge pull request #104 from sidhulyalkar/main

Update `model.PoseEstimation` to infer_output_dir ([`0f68e09`](https://github.com/datajoint/element-deeplabcut/commit/0f68e096cffdaf8f54701eda9bc636a5aa6168eb))

* update to create output_dir during pose estimation and update task ([`f53852d`](https://github.com/datajoint/element-deeplabcut/commit/f53852dc096bcf3d72ad5a6ffc3ada0c479ad9ae))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut ([`50f0d43`](https://github.com/datajoint/element-deeplabcut/commit/50f0d4310909b0c7a1b8d5e47efa374cb88a3c45))

* update yaml safe load in dlc_reader ([`b4a6ae0`](https://github.com/datajoint/element-deeplabcut/commit/b4a6ae0685b669741b2380c920b2df11305b02e5))

* update yaml safe loading ([`7c8ccdd`](https://github.com/datajoint/element-deeplabcut/commit/7c8ccdd5e421e3f218fb7a1d47459d344e580c80))

* Merge pull request #101 from sidhulyalkar/main

Update `snapshotindex` and `latest_snapshot` designation ([`7b4e66a`](https://github.com/datajoint/element-deeplabcut/commit/7b4e66aa991ecf1ba6dbedeb4ee131cf5d3e651d))

* modify snapshot index determination ([`556556b`](https://github.com/datajoint/element-deeplabcut/commit/556556bb5751e9b1d6d80e8655776c3fded6f412))

* modify latest snapshot determination ([`6278148`](https://github.com/datajoint/element-deeplabcut/commit/627814833d2005755cc011228dfc44faafbb0e17))

* modify snapshotindex assignment in model training ([`474269e`](https://github.com/datajoint/element-deeplabcut/commit/474269e94176c61a3b536c48916ef4fac1a887d9))

* Merge pull request #100 from sidhulyalkar/main

Modify training to update init_weights path ([`fcdb2ec`](https://github.com/datajoint/element-deeplabcut/commit/fcdb2ec085d609a50825b420d3a65f65ea26e2e6))

* update changelog ([`fcc7007`](https://github.com/datajoint/element-deeplabcut/commit/fcc700737d6c1ffa7f167a2ed2b76b6e85443dc2))

* update version ([`4543d08`](https://github.com/datajoint/element-deeplabcut/commit/4543d087ccf51540d77a8b04facd4664dc8fae3d))

* update to use deeplabcut.__path__ ([`935938e`](https://github.com/datajoint/element-deeplabcut/commit/935938e12a5892aba91951a516b5631221c270ff))

* update init_weights_path before training model ([`87e0aae`](https://github.com/datajoint/element-deeplabcut/commit/87e0aaeb197343937886dae992cf2ca08b37f560))

* Merge pull request #107 from MilagrosMarin/main

Add last PR changes to CHANGELOG, bump version, blackformatting `tests` ([`190150d`](https://github.com/datajoint/element-deeplabcut/commit/190150d78e1c4c47560a42afae47fa12905ea206))

* add last PR to CHANGELOG and bump version ([`9f8b212`](https://github.com/datajoint/element-deeplabcut/commit/9f8b21229873a2f12f5b2bd9f1241d5c11e97a21))

* blackformatting tests ([`a5ec467`](https://github.com/datajoint/element-deeplabcut/commit/a5ec467e1d5f6a446bb988f4f691466fc57c6587))

* delete PyPI release ([`9762a19`](https://github.com/datajoint/element-deeplabcut/commit/9762a193c707fe97bb6c062ca3aec25c5bd5a231))

* Merge pull request #106 from ttngu207/main

Add pytest ([`16c845e`](https://github.com/datajoint/element-deeplabcut/commit/16c845e030d5a686b36a40624a2dd832220bf671))

* Merge pull request #103 from MilagrosMarin/main

Update setup dependencies + fix YAML bug + fix diagram + fix typo in docstring + tutorial setup ([`499d85e`](https://github.com/datajoint/element-deeplabcut/commit/499d85ee4f3464e15783b5f66ec55f050567d1f6))

* add YAML object as recommended in parallel PR#102 ([`d6fe551`](https://github.com/datajoint/element-deeplabcut/commit/d6fe551450853c6adc44ea78ca1c05156c920209))

* Refactor YAML loader instant. for consistency ([`abc10df`](https://github.com/datajoint/element-deeplabcut/commit/abc10dff98312add528fcd2d0fbe456f0a976b5a))

* update `changelog` and `version.py` ([`cd358eb`](https://github.com/datajoint/element-deeplabcut/commit/cd358ebc2454b3c4a18b93bc149d16963607fe0f))

* black formatting `tutorial.ipynb` ([`fddad64`](https://github.com/datajoint/element-deeplabcut/commit/fddad646545466eaf98cac97fd165382f4593fb0))

* black formatting `dlc_reader.py` ([`d1b86ce`](https://github.com/datajoint/element-deeplabcut/commit/d1b86ceec40a50ac5288e01d2b7e680309a72d2d))

* from `safe_load` to `load` ([`9b61920`](https://github.com/datajoint/element-deeplabcut/commit/9b6192071c12d61f8386d6a95ba043bfd331ade6))

* update outputs of the tutorial notebook ([`0885f48`](https://github.com/datajoint/element-deeplabcut/commit/0885f480427fe4dc182204d0823e1236f110f9cb))

* Address the bug introduced by the latest update to the YAML dependency ([`fbab55d`](https://github.com/datajoint/element-deeplabcut/commit/fbab55d8bf32006fb0323d7c03fe4f5d5fc897a9))

* fix `input_dir` and `output_dir` in the tutorial ([`a50836d`](https://github.com/datajoint/element-deeplabcut/commit/a50836d0e8b8c3fd7c89ef2245730f7da2f83646))

* move `import os` from `__init__` to `tutorial_pipeline` ([`95e10df`](https://github.com/datajoint/element-deeplabcut/commit/95e10df1e859d37843a8242efaa20395b0c359ee))

* change name of `flowchart.svg` in notebook ([`a5e59e5`](https://github.com/datajoint/element-deeplabcut/commit/a5e59e52f5ddca108ef96d1cb806ab784dda6aa1))

* change name of flowchart as in element-ca-imaging ([`8e0d9dd`](https://github.com/datajoint/element-deeplabcut/commit/8e0d9dd25b49856d352e2b1edd6d42a1f007234c))

* minor change in dependency version in setup ([`ebe6f2b`](https://github.com/datajoint/element-deeplabcut/commit/ebe6f2bf83923c3ff0f0774e123912ca80941afb))

* minor update on tutorial markdowns as in array-ephys ([`cc0424c`](https://github.com/datajoint/element-deeplabcut/commit/cc0424cd34f3a0463cafe79c16b87ca65369d943))

* setup install directly from GitHub instead of PyPI ([`820711e`](https://github.com/datajoint/element-deeplabcut/commit/820711e7095be79af6c2e9c466a60b17dada7d01))

* move `dj.config()` from init to pipeline.py ([`28c55bc`](https://github.com/datajoint/element-deeplabcut/commit/28c55bcbea20c4859e58b7deb23d32efcaf3b668))

* Update `diagram_flowchart` as in array-ephys repo ([`ab3370a`](https://github.com/datajoint/element-deeplabcut/commit/ab3370a9fcfd456a603bce92b925509de1a0b446))

* update docstring for `model_description` varchar ([`3b635d6`](https://github.com/datajoint/element-deeplabcut/commit/3b635d68936cdbb00900ee2ffe5916148bce6cc5))

* Revert &#34;adjusted length of fields of varchar&#34;

This reverts commit cc24a03684a21be82ef56e70bc159b793fe2e66d. ([`71af568`](https://github.com/datajoint/element-deeplabcut/commit/71af568e947a8b73f8aed1ba4a39207888713c77))

* adjusted length of fields of varchar ([`cc24a03`](https://github.com/datajoint/element-deeplabcut/commit/cc24a03684a21be82ef56e70bc159b793fe2e66d))

* Merge pull request #97 from A-Baji/main

revert: :memo: revert docs dark mode cell text color ([`5b12e5e`](https://github.com/datajoint/element-deeplabcut/commit/5b12e5e85320fd8e9184eeec158dfce5d75374f5))

* revert: :memo: revert dark mode cell text color ([`be09507`](https://github.com/datajoint/element-deeplabcut/commit/be09507af0fef1bd2f714f702c3254ad9fe0b52f))

## v0.2.10 (2023-11-20)

### Unknown

* Merge pull request #99 from sidhulyalkar/main

Update Version and Changelog ([`11802ff`](https://github.com/datajoint/element-deeplabcut/commit/11802fff727a14c516e4e3d99cdd4bdcc8caec2e))

* update version and changelog ([`b67073d`](https://github.com/datajoint/element-deeplabcut/commit/b67073d4ffe1339bd3519d604de0e423a33bd7d0))

* Merge branch &#39;main&#39; of https://github.com/sidhulyalkar/element-deeplabcut ([`c0181c1`](https://github.com/datajoint/element-deeplabcut/commit/c0181c153a7fa3f017fd1ddbada2a22c03b9164b))

* Merge pull request #98 from MilagrosMarin/main

update `setup.py` to fix conflicting dependencies ([`fbd1ff6`](https://github.com/datajoint/element-deeplabcut/commit/fbd1ff6e94cd5d80e0b60a258de9f547fc2827e6))

* update setup.py to fix conflicting dependencies ([`1a2d262`](https://github.com/datajoint/element-deeplabcut/commit/1a2d2628e79e527de337ec5eb2df84bd5ea10f6b))

* Merge pull request #96 from ttngu207/element-dlc-test

update `snapshotindex` after training ([`887b571`](https://github.com/datajoint/element-deeplabcut/commit/887b571c5e5be6e56af2d83edf4add5f39145290))

* smarter transaction logic ([`8a1dff2`](https://github.com/datajoint/element-deeplabcut/commit/8a1dff2e8778cf71b42a8c10479186e932bb2aad))

* remove the `project_path` kwarg in `insert_new_model` ([`03c37d1`](https://github.com/datajoint/element-deeplabcut/commit/03c37d1d5ea10558972686c980f1cbd4c0373fbe))

* update `snapshotindex` after training ([`736f4d7`](https://github.com/datajoint/element-deeplabcut/commit/736f4d76b283169b782819fa7dcc32ef5891593d))

* remove opening of new transaction for insertion into model table ([`09a75cb`](https://github.com/datajoint/element-deeplabcut/commit/09a75cb5a2573238b53e6387b2783e3577e4c78d))

* Merge pull request #95 from MilagrosMarin/element-dlc-test

minor changes to standardize the elements ([`ded35b3`](https://github.com/datajoint/element-deeplabcut/commit/ded35b322fae98322bde3bea5f6bc4df29f4f819))

* Merge pull request #3 from kushalbakshi/dev

Black formatting ([`b33ece9`](https://github.com/datajoint/element-deeplabcut/commit/b33ece9c8c11ba150b0188bb8790f40561a90c37))

* Black formatting ([`85e38f2`](https://github.com/datajoint/element-deeplabcut/commit/85e38f27ecc4f8315b67982012ba3ec0ee7821fe))

* minor changes to mirror PR element-array-ephys ([`30a1b9c`](https://github.com/datajoint/element-deeplabcut/commit/30a1b9c908f48b28fc63a758e7fc6e3168b951ba))

* Merge pull request #93 from MilagrosMarin/element-dlc-test ([`1314488`](https://github.com/datajoint/element-deeplabcut/commit/131448823cc3852dc3cf6930007d6d9b1093a73b))

* Delete notebooks/demo.ipynb ([`9d5ca5a`](https://github.com/datajoint/element-deeplabcut/commit/9d5ca5a4aee94d3ec02b5f7f19f4fa29ee12259b))

* starting the demo notebook ([`eef6975`](https://github.com/datajoint/element-deeplabcut/commit/eef6975c9d7f7ad6f724249dc738d95ea327fc3e))

* update changelog and gitignore ([`741e2ce`](https://github.com/datajoint/element-deeplabcut/commit/741e2ce654a53f1eed05d393677aef618d5b7ff8))

## v0.2.9 (2023-10-26)

### Unknown

* Merge pull request #92 from MilagrosMarin/element-dlc-test

update `model.py`,tutorial notebook,`changelog`, and `version` ([`c887ab8`](https://github.com/datajoint/element-deeplabcut/commit/c887ab807785d16ef6dd48d0328b6e26bb984cd6))

* Update element_deeplabcut/model.py

Co-authored-by: Thinh Nguyen &lt;thinh@datajoint.com&gt; ([`fba8810`](https://github.com/datajoint/element-deeplabcut/commit/fba88107a8769e964d321f39462e2f25a43ffd20))

* delete debug lib ([`67b9015`](https://github.com/datajoint/element-deeplabcut/commit/67b90158481ec369fe84a85f54506272d2b6d191))

* update model.py ([`ca5acd1`](https://github.com/datajoint/element-deeplabcut/commit/ca5acd1931a819bf665f5657208b499144121c97))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut into element-dlc-test ([`fe423f2`](https://github.com/datajoint/element-deeplabcut/commit/fe423f2bd3dfbfd2ab113354dc8eb71ad3cf6719))

* Merge pull request #91 from datajoint/dev

Update tutorial and codespace ([`be8256f`](https://github.com/datajoint/element-deeplabcut/commit/be8256f03336eba2478885399357585a64ed50df))

* Merge pull request #90 from MilagrosMarin/element-dlc-test

Update the example data, environment variables, tutorial notebook and README ([`4a74fe4`](https://github.com/datajoint/element-deeplabcut/commit/4a74fe4258c131e5244c7c8983263ee5372364e1))

* Merge pull request #89 from MilagrosMarin/element-dlc-test

Merge `workflow-deeplabcut`&#39;s tutorial environment ([`55adb0e`](https://github.com/datajoint/element-deeplabcut/commit/55adb0e29fb6b5fe508684a2eac9758603f52cfc))

* update model.py: remove a line and update args ([`5e04d5f`](https://github.com/datajoint/element-deeplabcut/commit/5e04d5f4340fd1b0a27f4bf3664f102e98c60f96))

* Update CHANGELOG.md ([`de29eef`](https://github.com/datajoint/element-deeplabcut/commit/de29eefaf114d7b961191d3db8b12437dd518683))

* add summary section ([`73a1a4f`](https://github.com/datajoint/element-deeplabcut/commit/73a1a4f54f22915033839ff29114436430e657c2))

* Update CHANGELOG.md ([`e9dd1bd`](https://github.com/datajoint/element-deeplabcut/commit/e9dd1bd8cbcbd9c76575e35cf7677f3eec8f2cef))

* update tutorial with outputs included ([`3996ed7`](https://github.com/datajoint/element-deeplabcut/commit/3996ed76b532cf4eac736f44b3b52a8670b7b5e5))

* update the markdowns of tutorial - outputs cleared ([`7edff63`](https://github.com/datajoint/element-deeplabcut/commit/7edff63a59c5c0a4318a59b0b9ba75d508b91b84))

* update changelog and version ([`4bd81ec`](https://github.com/datajoint/element-deeplabcut/commit/4bd81ecb3f1279a39359cd8edb98ba922cb0a619))

* change in visualization plots ([`0fb7c05`](https://github.com/datajoint/element-deeplabcut/commit/0fb7c0515aab665e108c70d9174ac1810b8f7235))

* final draft with all outputs and minor changes ([`bb25140`](https://github.com/datajoint/element-deeplabcut/commit/bb2514088aab291abbd027017456e95602894c4d))

* final draft without output ([`5e942b6`](https://github.com/datajoint/element-deeplabcut/commit/5e942b609970c5687b0ea609d9d5674e72adb525))

* update tutorial draft ([`6d5011e`](https://github.com/datajoint/element-deeplabcut/commit/6d5011e174076f4925af2019a539878041de8acb))

* draft tutorial ([`828cd87`](https://github.com/datajoint/element-deeplabcut/commit/828cd87a377ede7ebd18bcd64cebfb0cf3bbc62e))

* correct the name of the pipeline figure ([`8ebd1f1`](https://github.com/datajoint/element-deeplabcut/commit/8ebd1f13e9ccfb0a1dcc7e017be71d3cc9f3a515))

* Merge pull request #1 from ttngu207/element-dlc-test

Element dlc test ([`04eb7eb`](https://github.com/datajoint/element-deeplabcut/commit/04eb7ebd64f58327e79bf829bb9fef2ee237b0a9))

* Merge branch &#39;element-dlc-test&#39; into element-dlc-test ([`a2b2fd2`](https://github.com/datajoint/element-deeplabcut/commit/a2b2fd28a3cdd1cb63fe082081d315f3e58dac3e))

* Add a tutorial quick test ([`f1fad23`](https://github.com/datajoint/element-deeplabcut/commit/f1fad23923588599750767203538e78fa83cd56b))

* add notebooks ([`94b2b17`](https://github.com/datajoint/element-deeplabcut/commit/94b2b17b47e8f9c1abba0104cbc596c4cf516153))

* update codespace and mounting strategy ([`477a355`](https://github.com/datajoint/element-deeplabcut/commit/477a355f5c63b88b3f2b19ed7436a8220715dd37))

* Update model.py ([`2f41aa3`](https://github.com/datajoint/element-deeplabcut/commit/2f41aa3f57a803d33a5695f1d4a1b0fd3f7a35e4))

* use `v2` example data ([`930c619`](https://github.com/datajoint/element-deeplabcut/commit/930c6195de33b7403278a05a7b70a1f7391ff9f5))

* Merge pull request #4 from MilagrosMarin/element-dlc-test

Element dlc test ([`299c4c1`](https://github.com/datajoint/element-deeplabcut/commit/299c4c18a8ded58df18c7d06fe2c76a0e29c6ab8))

* Update setup.py

Co-authored-by: Kushal Bakshi &lt;52367253+kushalbakshi@users.noreply.github.com&gt; ([`ed8de3a`](https://github.com/datajoint/element-deeplabcut/commit/ed8de3a9ce275d25fc9f680a780fccd000a25dc2))

* Update setup.py

Co-authored-by: Kushal Bakshi &lt;52367253+kushalbakshi@users.noreply.github.com&gt; ([`19dc567`](https://github.com/datajoint/element-deeplabcut/commit/19dc567a5d5121707d9f24256cbd26679431c9c6))

* Update setup.py

Co-authored-by: Kushal Bakshi &lt;52367253+kushalbakshi@users.noreply.github.com&gt; ([`2e49708`](https://github.com/datajoint/element-deeplabcut/commit/2e497081f3e9cc97b746ef67ab38963c476cf55d))

* Update README.md

Co-authored-by: Kushal Bakshi &lt;52367253+kushalbakshi@users.noreply.github.com&gt; ([`525924d`](https://github.com/datajoint/element-deeplabcut/commit/525924da99aabd040719a74e3633604141426e41))

* Update CONTRIBUTING.md

Co-authored-by: Kushal Bakshi &lt;52367253+kushalbakshi@users.noreply.github.com&gt; ([`1c7bec4`](https://github.com/datajoint/element-deeplabcut/commit/1c7bec4889b47dd00737567a86286c8ea890bb9c))

* Update .devcontainer/devcontainer.json

Co-authored-by: Kushal Bakshi &lt;52367253+kushalbakshi@users.noreply.github.com&gt; ([`61e73bf`](https://github.com/datajoint/element-deeplabcut/commit/61e73bfafd8f4874be990997d15dbbac4f75abf7))

* Update .devcontainer/Dockerfile

Co-authored-by: Kushal Bakshi &lt;52367253+kushalbakshi@users.noreply.github.com&gt; ([`61fbfea`](https://github.com/datajoint/element-deeplabcut/commit/61fbfea3b78c799d2ca97841ca865430f7708554))

* add current_project_folder env variable to __init_ ([`7980338`](https://github.com/datajoint/element-deeplabcut/commit/7980338699d33bbfcda4c6c6884f4e1404283a68))

* solve readme conflict ([`7ce6007`](https://github.com/datajoint/element-deeplabcut/commit/7ce600754d6301137e16bbddcd1622204671069a))

* Merge branch &#39;element-dlc-test&#39; of https://github.com/MilagrosMarin/element-deeplabcut into element-dlc-test ([`7a0ea4a`](https://github.com/datajoint/element-deeplabcut/commit/7a0ea4a3950b4a8aa836a30271eea73615db1c8c))

* Merge branch &#39;dev&#39; into element-dlc-test ([`c94f336`](https://github.com/datajoint/element-deeplabcut/commit/c94f33679d2837b7f8111816f56f5f199d27d917))

## v0.2.8 (2023-08-08)

### Test

* test: environments and volumes commented in yaml ([`2480421`](https://github.com/datajoint/element-deeplabcut/commit/2480421184aab57bc7a4d50874fb99df0e589107))

* test: change CaImaging image to build ([`e15b32f`](https://github.com/datajoint/element-deeplabcut/commit/e15b32fcf0ac0528ff557549e436476e937785b1))

* test: try with calcium imaging image ([`f9c8eaa`](https://github.com/datajoint/element-deeplabcut/commit/f9c8eaa377f80c7b68e4f8c796b01b6d33536028))

* test: no volumes workspaces dlc ([`ed8c1cc`](https://github.com/datajoint/element-deeplabcut/commit/ed8c1ccf77ac1df3a530b68bbc3a366aad14cea1))

* test: Revert two minor comments in dockerfile ([`160a32e`](https://github.com/datajoint/element-deeplabcut/commit/160a32e7a00aa5ddbed0bab3aebac20a2ed6fd53))

* test: from python short command in dockerfile ([`2a394ae`](https://github.com/datajoint/element-deeplabcut/commit/2a394aee22dab16f2a9f18d5ba3741bc64f999f5))

### Unknown

* Merge pull request #88 from kabilar/main ([`fce53d3`](https://github.com/datajoint/element-deeplabcut/commit/fce53d309a806921eefef7025be18c0ffae480f4))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut into main ([`53835e2`](https://github.com/datajoint/element-deeplabcut/commit/53835e25eaeb6173eba65749866fc572574007d1))

* Merge pull request #86 from kabilar/main

Update GitHub Actions and Readme ([`5a76c6c`](https://github.com/datajoint/element-deeplabcut/commit/5a76c6c9aacc99370b8b1fccaddced91b42a74ed))

* Update version for release ([`f8fde49`](https://github.com/datajoint/element-deeplabcut/commit/f8fde492b64a59e72f6ea0238e530619839cc063))

* Merge &#39;main&#39; of datajoint/element-deeplabcut ([`8ca047d`](https://github.com/datajoint/element-deeplabcut/commit/8ca047d1a6d77a294f1d444695abd8a2e228db66))

* Format with black ([`b16c386`](https://github.com/datajoint/element-deeplabcut/commit/b16c3861c5a4f51aaabb6300999b0fc4a0b92641))

* Format with black ([`f37a17f`](https://github.com/datajoint/element-deeplabcut/commit/f37a17f2f59bc974b82b6d4c0dffbde72be34ec1))

* Update changelog ([`dff5b87`](https://github.com/datajoint/element-deeplabcut/commit/dff5b8776d12dc3c9332f60514fa926f7e3b12ae))

* Update readme ([`fcd026a`](https://github.com/datajoint/element-deeplabcut/commit/fcd026a86be2d22d74f70a5ffdd6a82de1a77626))

* Rename images ([`cc2cbfc`](https://github.com/datajoint/element-deeplabcut/commit/cc2cbfcbc79fc38da6fe2eadcad189c9732190d4))

* Update GitHub Actions ([`ac3f334`](https://github.com/datajoint/element-deeplabcut/commit/ac3f334f00710c82c10a7432c2e9ce3310b6bee9))

* update README based on ca-imaging element ([`cbc6e27`](https://github.com/datajoint/element-deeplabcut/commit/cbc6e2724357ecb59a61214edf6ee103ee5111f1))

* update current_project_folder-&gt;from_top_tracking ([`c0b6ed2`](https://github.com/datajoint/element-deeplabcut/commit/c0b6ed23e43981d7ac40f7b2aa7c8f695f321354))

* update flowchart URL ([`07522a7`](https://github.com/datajoint/element-deeplabcut/commit/07522a7a6330268c80371e87a8c7cc8838e8e6fc))

* rename image names to mirror ca-imaging ([`0df510d`](https://github.com/datajoint/element-deeplabcut/commit/0df510d88c712d779a2b6c1242866cf4b7c898a9))

* Images from workflow-don&#39;t match the `element` ([`5b317a9`](https://github.com/datajoint/element-deeplabcut/commit/5b317a91d72a5548699edde48fb81d134c77b19a))

* revert model.py and train.py to add in next PR ([`1e6c27e`](https://github.com/datajoint/element-deeplabcut/commit/1e6c27ed0dce5e35ea713d26c64dd2008ba81482))

* Add `env` variables and prefix to dj database ([`1969e59`](https://github.com/datajoint/element-deeplabcut/commit/1969e5911b5aa6e56be908e1124cd95d4d91949d))

* revert removing files in `element-deeplabcut` ([`49f2b2f`](https://github.com/datajoint/element-deeplabcut/commit/49f2b2f011981db8c345093bef685faf03c1f8c9))

* SCIOPS-59 &amp; add two dependencies in setup ([`f30425f`](https://github.com/datajoint/element-deeplabcut/commit/f30425fbf30eae728f9e8926587a04aaac7d8c41))

* delete comments in dockerfile ([`8511b4e`](https://github.com/datajoint/element-deeplabcut/commit/8511b4ea3efea1f0b1d6dc939048cc0c13f5a30d))

* add s3fs postcommand in devcontainer ([`89df0f4`](https://github.com/datajoint/element-deeplabcut/commit/89df0f4bdaacdf5d59a7a679b65155ac0fa1a5b2))

* update dj_public_s3_location in docker-compose ([`60f1a81`](https://github.com/datajoint/element-deeplabcut/commit/60f1a814750efd1cac7ac09cddbdfd7db2548169))

* Merge branch &#39;element-dlc-test&#39; of https://github.com/MilagrosMarin/element-deeplabcut into element-dlc-test ([`895dbd2`](https://github.com/datajoint/element-deeplabcut/commit/895dbd24bb2710a65ac1b4037767e2eb61f8e76d))

* Update .github/ISSUE_TEMPLATE/config.yml

Co-authored-by: Kushal Bakshi &lt;52367253+kushalbakshi@users.noreply.github.com&gt; ([`80100db`](https://github.com/datajoint/element-deeplabcut/commit/80100db00493c4d19dfa806efbd9d8dcb336df8e))

* fix bug using &#39; &#39; in extra_require in setup.py ([`89fd674`](https://github.com/datajoint/element-deeplabcut/commit/89fd6746d29d53bf26a6d441e59223351d50143e))

* Merge branch &#39;element-dlc-test&#39; of https://github.com/MilagrosMarin/element-deeplabcut into element-dlc-test ([`722edc1`](https://github.com/datajoint/element-deeplabcut/commit/722edc1df6c0cbacb3939e6c5eb769691ed9a259))

* Update .github/workflows/test.yaml

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`38587c8`](https://github.com/datajoint/element-deeplabcut/commit/38587c85c0ca394d5ecd260d0bc5d11bbf317fd3))

* restore docs/ directory ([`735a1cb`](https://github.com/datajoint/element-deeplabcut/commit/735a1cb8c4641e4e319e4e6bc9b12b0cb3441bc1))

* Update setup.py for DLC in M2 MacOS ([`84e09d9`](https://github.com/datajoint/element-deeplabcut/commit/84e09d9919133e58d1ed63442563e3bfd679f491))

* Merge branch &#39;element-dlc-test&#39; of https://github.com/MilagrosMarin/element-deeplabcut into element-dlc-test ([`48e73e4`](https://github.com/datajoint/element-deeplabcut/commit/48e73e48e518fa841b8dd98aa916fa27447db8f3))

* Update setup.py ([`f040971`](https://github.com/datajoint/element-deeplabcut/commit/f040971843bdabb3cecf098c972bbf76cb15e954))

* Install deeplabcut ([`ae8ce7d`](https://github.com/datajoint/element-deeplabcut/commit/ae8ce7d402173a7aa591e2e3fc1b6dba8ebdea28))

* updated libraries in mchips installation ([`3480270`](https://github.com/datajoint/element-deeplabcut/commit/3480270c153ea015cf7bed0013403a96e0bbfbf8))

* test minor change in dependencies in dockerfile ([`f5eaae4`](https://github.com/datajoint/element-deeplabcut/commit/f5eaae46bd466d35c074945bd106ef80426e9df2))

* Test codespaces: #depend.reduced, lines commented ([`f74a497`](https://github.com/datajoint/element-deeplabcut/commit/f74a497315230151f6eb5f4c8ae4a2b1f1f4fe20))

* delete redundancy ([`9f816fb`](https://github.com/datajoint/element-deeplabcut/commit/9f816fbe7e7e1b83d8e0f7deae61d0ac5ffbc9a6))

* test `dlc_default` in `Dockerfile` ([`bd8f57c`](https://github.com/datajoint/element-deeplabcut/commit/bd8f57c14f1910f5181bc11ca8729ebe7f219a10))

* update `dockerfile` and `setup` ([`6359f06`](https://github.com/datajoint/element-deeplabcut/commit/6359f0681c9ac1c4f10325e7c45ce94b0382a877))

* update `.yaml` files ([`5a01ace`](https://github.com/datajoint/element-deeplabcut/commit/5a01aceb3f2a95b133bf068da0cc357c2191b31a))

* update `.gitignore` ([`ef0099c`](https://github.com/datajoint/element-deeplabcut/commit/ef0099c2f3f36c9f4644ee16a6834c799d4992b3))

* update code_conduct, contrib and license files ([`421e49d`](https://github.com/datajoint/element-deeplabcut/commit/421e49dc9ff295357dd978b10b25e968523ed5e5))

* update`.github` directory ([`0eb7c3a`](https://github.com/datajoint/element-deeplabcut/commit/0eb7c3a372623a460f8552970e27660dfdd483bc))

* minor change in dockerfile ([`c79f3f3`](https://github.com/datajoint/element-deeplabcut/commit/c79f3f3acc8ae640493be61bdcd7470b6c02ed7e))

* Delete `.github` directory from this PR ([`ead5b39`](https://github.com/datajoint/element-deeplabcut/commit/ead5b39fd050af7afa2a6cba19021bce7ac59371))

* Delete `docs` directory from this PR ([`0b17199`](https://github.com/datajoint/element-deeplabcut/commit/0b17199d2fabf0bfd3bb3d821691610dac342d24))

* Major changes for PR codespace environment ([`842561f`](https://github.com/datajoint/element-deeplabcut/commit/842561f9af1b5ef1629cf5386cd44665395ce98e))

* Merge remote-tracking branch &#39;origin/element-dlc-test&#39; into element-dlc-test ([`6001819`](https://github.com/datajoint/element-deeplabcut/commit/600181980f76c30fad11fcae80b2bffb34bd7038))

* removed more files from git ([`845974a`](https://github.com/datajoint/element-deeplabcut/commit/845974af467629120d160db2f8fea29051a99a02))

* Recover files from git rm ([`276487b`](https://github.com/datajoint/element-deeplabcut/commit/276487b91823a31600bf82f184b062517b1c2d7b))

* change DLC_ROOT_DATA_DIR to example_data directory ([`3166830`](https://github.com/datajoint/element-deeplabcut/commit/316683090f0d37f99806fd1aff18a0606a14b317))

* removed files from git ([`da33fd4`](https://github.com/datajoint/element-deeplabcut/commit/da33fd4640ac6a21b5033b27fef1c2e68a7dacd7))

* dockerfile new env for dlc folder ([`e0fb8d3`](https://github.com/datajoint/element-deeplabcut/commit/e0fb8d38af32f9af1ce7ea43731a206f9a91a045))

* uncomment env&amp;volumes but changed to element-dlc ([`9354ac1`](https://github.com/datajoint/element-deeplabcut/commit/9354ac1bdcb8e171936e4a0d7910b35db1b839bd))

* from IMAGING_ROOT_DATA_DIR to DLC_ROOT_DATA_DIR ([`9551723`](https://github.com/datajoint/element-deeplabcut/commit/955172331f11d3d77fe09e4fe624f4501b6d440f))

* setup comments deleted ([`da33b01`](https://github.com/datajoint/element-deeplabcut/commit/da33b010f96aff64ede616b6dd5dfb2dbb53fe62))

* use FROM with base image without digest ([`42fa38c`](https://github.com/datajoint/element-deeplabcut/commit/42fa38cd1e89acd6480c999f195da7eb59b1f188))

* test dockerfile:  imaging_root_data_dir not needed ([`30c3dff`](https://github.com/datajoint/element-deeplabcut/commit/30c3dff84b0a78bcd289815bbab1bec5d49bc898))

* revert dockerfile ([`ebfea90`](https://github.com/datajoint/element-deeplabcut/commit/ebfea90edf72c14ce054b4c34a1b1d81eadbc44e))

* setup.py: delete code line about requirements.txt ([`a5a13f9`](https://github.com/datajoint/element-deeplabcut/commit/a5a13f97ffe22601d4ab000b5db207a15a105b29))

* apt-utils and apt-get in dockerfile ([`8901870`](https://github.com/datajoint/element-deeplabcut/commit/89018704e863c6b4977ae640f057de4bf67d3eba))

* uncomment volumes in docker config file ([`8a8d704`](https://github.com/datajoint/element-deeplabcut/commit/8a8d704a324379bc5dc0c98b2467cd81434631d6))

* add `context` in docker yaml as well ([`6133ca7`](https://github.com/datajoint/element-deeplabcut/commit/6133ca7fd4ed77f25ee320a7c8e79da966e4ddd5))

* use build instead of image to test the dev cont ([`2957160`](https://github.com/datajoint/element-deeplabcut/commit/2957160cd50e6e5de59df7b32321f7e6f83303be))

* comment `environment` line with previous commit ([`d0088ed`](https://github.com/datajoint/element-deeplabcut/commit/d0088ed171c5217840ae0f8d60d40fc6fab01c36))

* comment &#39;S3 location&#39; for DLC-v1 to test dev ([`61aa180`](https://github.com/datajoint/element-deeplabcut/commit/61aa1800c39e3e90e1d788ab764021e748202443))

* comment `image element_dlc` code line before merge ([`4820f75`](https://github.com/datajoint/element-deeplabcut/commit/4820f759ca42e042dad212139e7331b52e9f35a6))

* dockerfile and devcontainer files for element-dlc ([`0973437`](https://github.com/datajoint/element-deeplabcut/commit/0973437784e5f566dcf2f9e921ba0779f9e8a7bd))

* important change to install dlc[apple_mchips] ([`1ef12f9`](https://github.com/datajoint/element-deeplabcut/commit/1ef12f95b9eea0995c093c4662ef93335e0e840f))

* change name for clarity to get_trajectory function ([`18daef4`](https://github.com/datajoint/element-deeplabcut/commit/18daef44a12cecbbccdb4a3627c307e8efebe6a4))

* add skip_duplicates to generate function ([`f774713`](https://github.com/datajoint/element-deeplabcut/commit/f77471395d07096450d17e34ce29ebeaaf328b92))

* Fix:generate triggers getattribute with model_name ([`745f5d4`](https://github.com/datajoint/element-deeplabcut/commit/745f5d4e2aab7f630f79390a7b5ed09399088b2c))

* processed_dir can not exist - bug fixed ([`b0ea7d4`](https://github.com/datajoint/element-deeplabcut/commit/b0ea7d451d7bb33bfd4f5b7758346b4d1abdedc2))

* Tutorial: major changes &amp; network training tested ([`4e2a7eb`](https://github.com/datajoint/element-deeplabcut/commit/4e2a7eb020dde70cdf0db863bcc42b394b6a29a0))

* Update intro tutorial notebook ([`3a2eba8`](https://github.com/datajoint/element-deeplabcut/commit/3a2eba8767cfee13923bb1963be72775a2006d7f))

* Update name from `pipeline` to `tutorial_pipeline` ([`5f50b4b`](https://github.com/datajoint/element-deeplabcut/commit/5f50b4b61d05f5e3fb9ea82bde0706c0e031ff5e))

* Merge &#39;main&#39; of datajoint/element-deeplabcut ([`97b676a`](https://github.com/datajoint/element-deeplabcut/commit/97b676acf98db0b51aeb2550ba74806b04014009))

## v0.2.7 (2023-08-04)

### Unknown

* Merge pull request #87 from MilagrosMarin/train_bug

Fix project path in the pose config file ([`78ac980`](https://github.com/datajoint/element-deeplabcut/commit/78ac98079332a6044497fc5b64d3f7c220903901))

* Fix project path ([`81eb296`](https://github.com/datajoint/element-deeplabcut/commit/81eb29654b202bbb324908ccb4e68c9dc66a58d3))

* [WIP] Update notebook and mac requirements ([`d6dad59`](https://github.com/datajoint/element-deeplabcut/commit/d6dad5989c36425e67b648968af1185c469f9ff1))

* Update requirements configuration ([`ca01071`](https://github.com/datajoint/element-deeplabcut/commit/ca010719f011ce82b7e5c7d82bb95708784758de))

* merge paths and pipeline files, move to notebooks ([`be51282`](https://github.com/datajoint/element-deeplabcut/commit/be51282812e58cb96d2bfcc9e7bb34d46ab39475))

* Rename `03-process` -&gt; `tutorial` ([`22cb379`](https://github.com/datajoint/element-deeplabcut/commit/22cb3794caf9e44fd988bc36e853e95844ec9e62))

* Remove jupytext scripts and workflow version ([`9c123b5`](https://github.com/datajoint/element-deeplabcut/commit/9c123b5b562ded14e5c8a71c6e3ad18b373f742b))

* Move workflow pipeline files ([`0135a38`](https://github.com/datajoint/element-deeplabcut/commit/0135a381a36d60dde0c7e45a51ce725cbb5beefd))

* Merge  &#39;datajoint/workflow/main&#39; into element ([`048c707`](https://github.com/datajoint/element-deeplabcut/commit/048c7071cb24e3a11d300475769d7cfdeec45e7e))

* Merge pull request #20 from kabilar/main

Add GitHub Actions workflows ([`205b5aa`](https://github.com/datajoint/element-deeplabcut/commit/205b5aa4acfeb27c9e65ced16e01e3759f1c1947))

* Update changelog ([`11f6773`](https://github.com/datajoint/element-deeplabcut/commit/11f6773d4ba8a3e90ec9c913d45bc14aefa497bd))

* Add GitHub Actions workflows ([`a6b2c9f`](https://github.com/datajoint/element-deeplabcut/commit/a6b2c9fc9bca604f02adda7ae3a40fdfa3926a44))

* Merge pull request #19 from kabilar/main

Update requirements for released packages ([`299eb37`](https://github.com/datajoint/element-deeplabcut/commit/299eb378c42bfd3560fa87f053af4b9339511355))

* Remove element-interface installation from source ([`e1d82b2`](https://github.com/datajoint/element-deeplabcut/commit/e1d82b247f6421bb9703dba62288b2cbba5043d1))

* Update command ([`836a4e2`](https://github.com/datajoint/element-deeplabcut/commit/836a4e2b9fba7d05565eeecbe338347961590bb8))

* Update changelog ([`f9d56eb`](https://github.com/datajoint/element-deeplabcut/commit/f9d56ebb19c6e1b93911a7416aa23bdeaa80e3ee))

* Update requirements ([`415145c`](https://github.com/datajoint/element-deeplabcut/commit/415145c1b00183623a8e1ac1766f0e05b9702f3f))

* Merge pull request #18 from CBroz1/main

Remove buggy EOF markers from DLC outputs in notebooks for mkdocs rendering ([`1f93e11`](https://github.com/datajoint/element-deeplabcut/commit/1f93e1128a4aceab1ba462c49277cc8d2976cea5))

* 🐛 Debug mkdocs notebooks rendering 2 ([`3a6a635`](https://github.com/datajoint/element-deeplabcut/commit/3a6a635f1f21b579b32ece2b345c1002bdbb4ffc))

* 🐛 Debug mkdocs notebooks rendering ([`43635d5`](https://github.com/datajoint/element-deeplabcut/commit/43635d5b06b3827bf26172e7e206c4f41232b8ef))

* Merge pull request #17 from tdincer/main

Update README.md ([`9d015e5`](https://github.com/datajoint/element-deeplabcut/commit/9d015e5946844b56805690a3543cda6fe79a3cab))

* Update README.md ([`32511f9`](https://github.com/datajoint/element-deeplabcut/commit/32511f92cb21773e5862d185b5891818ddd96188))

* Merge pull request #16 from kushalbakshi/main

Fixed typo in README ([`9ce9aef`](https://github.com/datajoint/element-deeplabcut/commit/9ce9aef6283292a61953a1634a5221bcb3068706))

* Fixed typo in README ([`5a3a1e5`](https://github.com/datajoint/element-deeplabcut/commit/5a3a1e5361115b757a4c886be1328ad99cb4e094))

* Merge pull request #15 from CBroz1/main

Add remaining suggestion from #14 ([`5e7fedd`](https://github.com/datajoint/element-deeplabcut/commit/5e7fedd6ae1833f0564566ccb3bdac7f98ce284a))

* Fix typo ([`872d9a0`](https://github.com/datajoint/element-deeplabcut/commit/872d9a0bda2ca0f337a3d151ce28b2cfa798df47))

* Add remaining suggestion from #14 ([`d1dee80`](https://github.com/datajoint/element-deeplabcut/commit/d1dee80467ff71ac9740c0436a5973ad6ecbce57))

* Merge pull request #14 from CBroz1/main

Docstrings -&gt; Google style for mkdocs render ([`ba2667e`](https://github.com/datajoint/element-deeplabcut/commit/ba2667e488d66848802b11ccc62fa85371a566d6))

* Update CHANGELOG.md ([`a836e0a`](https://github.com/datajoint/element-deeplabcut/commit/a836e0abf2c1cab9a832afc1a7a1586cb8f2579e))

* Update README.md

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`2913c86`](https://github.com/datajoint/element-deeplabcut/commit/2913c8642bc70c641dadd1d2a3e0d7b3e444ce70))

* Update CHANGELOG.md

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`3eec272`](https://github.com/datajoint/element-deeplabcut/commit/3eec2720dfeb206e129b52e8c11f5c0f19fcf230))

* Update changelog. Add attribs to Device ([`6584958`](https://github.com/datajoint/element-deeplabcut/commit/65849581b46fa7f21702fb5e025aae8286c2c51a))

* Add class docstring for Device ([`b141b1e`](https://github.com/datajoint/element-deeplabcut/commit/b141b1e0d7144d72c3d43232abcb4f7e5f9faacb))

* Simplify README, direct to new docs site ([`60997af`](https://github.com/datajoint/element-deeplabcut/commit/60997afeecb3a7f2bbcf5648ae7a4d9e56adbd8c))

* Add typing info for mkdocs ([`a729432`](https://github.com/datajoint/element-deeplabcut/commit/a729432694cb62eaa1564246901011cb87c5eee5))

* Docstrings -&gt; Google style for mkdocs render ([`d7ba7e8`](https://github.com/datajoint/element-deeplabcut/commit/d7ba7e87589a06ac4a9162256a41bee13914ac0b))

* Merge pull request #12 from CBroz1/dev

Integration tests ([`c6ff6d6`](https://github.com/datajoint/element-deeplabcut/commit/c6ff6d64981b8612c9db816bce61bb9342882675))

* Apply suggestion from code review

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`edbff23`](https://github.com/datajoint/element-deeplabcut/commit/edbff23933ecd98bb1b9833291bdbd8d3db87c0e))

* WIP: Fix docker ([`a0a76e9`](https://github.com/datajoint/element-deeplabcut/commit/a0a76e942a89d52b80bff314a4fa1a20cbda97c1))

* WIP: add visualization notebook ([`698105e`](https://github.com/datajoint/element-deeplabcut/commit/698105e03184624997f1b71716f32a7faf6e25d3))

* WIP: revise notebooks for new dataset ([`7fa0ddb`](https://github.com/datajoint/element-deeplabcut/commit/7fa0ddb202cd55fb551727e9372f123d95add769))

* WIP: jupysync ([`295df7e`](https://github.com/datajoint/element-deeplabcut/commit/295df7ea42b74e43da47d21f7f59011bda6bd1e1))

* WIP: docker edits. notebook revamp. incomplete ([`6b12b85`](https://github.com/datajoint/element-deeplabcut/commit/6b12b851f4be28b1fb340474531e2a5636324e54))

* WIP: minor cleanup ([`af90a61`](https://github.com/datajoint/element-deeplabcut/commit/af90a612c5259c134dc3da37d8f42481bc8010b2))

* WIP: all tests pass locally ([`c1aa455`](https://github.com/datajoint/element-deeplabcut/commit/c1aa455c6a51e4b95523ca0d9e172c1ffe524b46))

* WIP: More integration tests. See details.

Currently can take MVP data and can expand.
Added - More population assertions for file create time
Added - Load_demo_data function for updating training config
      - If added to element, could continue training from prev step
Modified - Device to lookup table for auto-contents
Updated - str_to_bool change source due to depreciation ([`33e92b4`](https://github.com/datajoint/element-deeplabcut/commit/33e92b4261c8e9eac55c38c10f3a83d376a68e1b))

* WIP: Integration tests. See details.

test_ingest: add table length and content assertions
test_populate: added - Not yet working
user_data/*csv: add metadata from new dataset
ingest.py: separate `get_dlc_items` by sub-function to call within tests
    ingest_train_params
    ingest_model
paths.py: return none if no output dir selected
pipeline.py: Equipment-&gt;Device
load_demo_data.py: add functions for expanding mvp dataset
    generate training dataset deterministic files
    generate absolute paths across configs ([`5425bcf`](https://github.com/datajoint/element-deeplabcut/commit/5425bcfdac9e121f7fc2d3fd39ec032f5e20c837))

* WIP: migrate fixtures to conftest.py ([`c7ffd43`](https://github.com/datajoint/element-deeplabcut/commit/c7ffd4393626b2c47f473630d1c24be024620a2f))

* WIP: Remaining files from prev commit ([`2226891`](https://github.com/datajoint/element-deeplabcut/commit/222689111a5abc6342d0f825c22e8366be1259a9))

* WIP. See details.

Parameterize DockerFile - move option selection to env
Refactor pytests - add setup.cfg to pass default params
Add Code of Conduct
Refactor ingest.py to ...
    1. provide subfuncs by schema
    2. add verbosity flag
    3. update docstrings ([`d2aa171`](https://github.com/datajoint/element-deeplabcut/commit/d2aa171e17d319bbe298f62a9a590ed67b9953ac))

* Merge pull request #11 from CBroz1/dj

blackify ([`0e76b79`](https://github.com/datajoint/element-deeplabcut/commit/0e76b793e5ddc6ca6b6fe3166abded40ee095ab5))

* Bump version ([`7f02a96`](https://github.com/datajoint/element-deeplabcut/commit/7f02a9607cda3e77d36e3b9b3eb801d9f8532414))

* blackify ([`c692fc5`](https://github.com/datajoint/element-deeplabcut/commit/c692fc52aedcd346ca7e6e9539aa3c6bf0baa18d))

* Merge pull request #8 from CBroz1/main

Updates for element PR #15 `RecordingInfo` table ([`4eeb86a`](https://github.com/datajoint/element-deeplabcut/commit/4eeb86a548e2a981e1050ef7a3c7d061deaa171c))

* Update workflow_deeplabcut/process.py

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`6eaf310`](https://github.com/datajoint/element-deeplabcut/commit/6eaf3105d3c328ea029305277acf31b654422ee0))

* Update workflow_deeplabcut/process.py

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`089e5a4`](https://github.com/datajoint/element-deeplabcut/commit/089e5a468391bd6228906ac52a3974d81192627c))

* Update workflow_deeplabcut/process.py

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`ddbd725`](https://github.com/datajoint/element-deeplabcut/commit/ddbd7250a18ecebc88d041f355aa38b562a19ac8))

* Apply suggestion from code review

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`345dd98`](https://github.com/datajoint/element-deeplabcut/commit/345dd98cc38d6884ada9d46f80ac55ad1a334855))

* Add element_interface.utils.ingest_csv_to_table ([`dd10089`](https://github.com/datajoint/element-deeplabcut/commit/dd1008930395c718c2fc478c2229db82c83bdf0d))

* Apply suggestions from code review

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`ac63549`](https://github.com/datajoint/element-deeplabcut/commit/ac635495ead4dadc0cae4d7672efad9ac7d7dd50))

* Merge from cbroz1:main ([`b414498`](https://github.com/datajoint/element-deeplabcut/commit/b414498dc9e97c45e141c451d1be06dfade7fa55))

* Apply suggestion from code review

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`04bc842`](https://github.com/datajoint/element-deeplabcut/commit/04bc842a0f97c91a64e6333781cc2792529892e9))

* Generalize equipment table ([`c828244`](https://github.com/datajoint/element-deeplabcut/commit/c828244dcbfc6f24ef26d763f0d4dcae091d5c7a))

* Merge branch &#39;main&#39; of https://github.com/datajoint/workflow-deeplabcut ([`a18fedf`](https://github.com/datajoint/element-deeplabcut/commit/a18fedf46cb245fc094e0bad15b88c869dc4cb0b))

* Merge pull request #7 from kabilar/main

Update README ([`1df9bf0`](https://github.com/datajoint/element-deeplabcut/commit/1df9bf0883f6f743bc3c492a04968bc8de467f2f))

* Update format ([`fdd12ac`](https://github.com/datajoint/element-deeplabcut/commit/fdd12ac243ec652c5011e1d2f257612de28f8635))

* Fix format ([`0253e7e`](https://github.com/datajoint/element-deeplabcut/commit/0253e7e545306dd44d1ee04ec009211bb9aaffc0))

* Add link to element.datajoint.org ([`8584969`](https://github.com/datajoint/element-deeplabcut/commit/85849698a213efca4eea3e2cacdee7b557269139))

* Update text ([`e60d017`](https://github.com/datajoint/element-deeplabcut/commit/e60d017a719b4c1f04772df8fddd3be784c74ef7))

* Fix format ([`11991b1`](https://github.com/datajoint/element-deeplabcut/commit/11991b1ea807a6fa10a562b2893448c9a9b236f1))

* Add links ([`2417a4b`](https://github.com/datajoint/element-deeplabcut/commit/2417a4be377cd384910282cb0e48a538e49e4fc1))

* Remove upstream element images to shorten readme ([`0e19c7f`](https://github.com/datajoint/element-deeplabcut/commit/0e19c7fe1fa1ec88f5ca9d8fe2b5bc792aeb806c))

* Add links to elements.datajoint.org ([`886d3f4`](https://github.com/datajoint/element-deeplabcut/commit/886d3f4a6dc8de49bdd711cd997b9f40b06c6273))

* Add citation section ([`4317fd7`](https://github.com/datajoint/element-deeplabcut/commit/4317fd77a5b81195ea52b38a2cf17f5f15685894))

* updates corresponding to element-deeplabcut PR #15 ([`2259f3a`](https://github.com/datajoint/element-deeplabcut/commit/2259f3a35914435a6f48376cce967560b14d520e))

* Merge pull request #6 from kabilar/main

Add issue templates ([`bcc4eb9`](https://github.com/datajoint/element-deeplabcut/commit/bcc4eb9e67fa73de5cfbeb2fe9c62d60da6c279d))

* Add issue templates ([`3c4fe47`](https://github.com/datajoint/element-deeplabcut/commit/3c4fe47707b1ecde71edc5df37cd340d5191b61b))

* Merge pull request #5 from CBroz1/main

minor README updates ([`9a5a1d8`](https://github.com/datajoint/element-deeplabcut/commit/9a5a1d8256c0cbfd86ab13de0b2be47786185e44))

* Update README.md from code review suggestion

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`20e0f06`](https://github.com/datajoint/element-deeplabcut/commit/20e0f0691a978b7200c75195c7786e932204787d))

* minor README updates ([`2003826`](https://github.com/datajoint/element-deeplabcut/commit/20038267292149114b6787d34d79e79f2b582aad))

* Merge pull request #2 from CBroz1/main

Pushing from `cbroz1:dev` discussion to `datajoint:main` ([`981415c`](https://github.com/datajoint/element-deeplabcut/commit/981415c0e02c5d610903802d0fa7be18fa3d3edf))

* Merge pull request #2 from CBroz1/dev

Update schema split: `train`, `model` ([`8095081`](https://github.com/datajoint/element-deeplabcut/commit/80950818bb9ca4b1911260157a419919c1f1c3fd))

* add `Session = session.Session` to pipeline.py, from code review ([`ff7cf58`](https://github.com/datajoint/element-deeplabcut/commit/ff7cf589bdabacf5137cb14a7264e5a00a002600))

* Update notebooks for separate video tables across schemas ([`d0d94b6`](https://github.com/datajoint/element-deeplabcut/commit/d0d94b60aaabb62cf8ddbc2f8921db8cc851f2c8))

* revise version info ([`4338899`](https://github.com/datajoint/element-deeplabcut/commit/4338899b0e9284e0afc975f0426ad344dc93d0d6))

* See details. Docker, Notebooks, JupyText, ingest.py

Update docker
Update NBs for 2 schema split
Add jupytext py files
Update ingest to reflect VideoRecording in pipeline
Add ingest feature for train.VideoSet ([`4bbdfc0`](https://github.com/datajoint/element-deeplabcut/commit/4bbdfc062b2e258dc35d14f3ecf5dde520963466))

* Split dlc schema ([`21f7494`](https://github.com/datajoint/element-deeplabcut/commit/21f74946b52edc6cbd453e5d72e38b158714b04b))

* update NBs 0 - 3 ([`bbf2d5d`](https://github.com/datajoint/element-deeplabcut/commit/bbf2d5df30c29f854ebc632c0604e9d787a07e1b))

* Draft notebooks. WIP Integration Tests ([`4c9cae1`](https://github.com/datajoint/element-deeplabcut/commit/4c9cae12a90801a0e41c1df7f226b3e87170239f))

* See Details

- README - add install instructions
- Notebook/1_Explore - major revision demonstrating new helper functions
- user_data - revise per table redesign
- ingest.py revise for paramset redesign
- paths.py
    - remove get_session_directory
    - remove arg from get_dlc_processed_dir
- pipeline.py minor change per paths change above ([`365a090`](https://github.com/datajoint/element-deeplabcut/commit/365a090fd3cc63f8bcd071ab82b97aaf4ee9ac7a))

* recordings.csv edit for new dev ([`4daf262`](https://github.com/datajoint/element-deeplabcut/commit/4daf26206cc5e73cc17c078784e0a77d0ee7fb45))

* new notebook for modeling use ([`598b0e2`](https://github.com/datajoint/element-deeplabcut/commit/598b0e2974a92d0d6de9c6543be9f8fc0c883a1d))

* draft ingest edits ([`3a3ba77`](https://github.com/datajoint/element-deeplabcut/commit/3a3ba77080d6aee2d3a530e2b5f481584ce19d74))

* Merge from CBroz1/dev

Recent work ([`99859a6`](https://github.com/datajoint/element-deeplabcut/commit/99859a659815556b392c844f324074359609ff1b))

* README+CHANGELOG clarity ([`8e7ca78`](https://github.com/datajoint/element-deeplabcut/commit/8e7ca78d861c500ae73416479fc7f8b36e0abd86))

* Cleanup: README, versioning, add ToDo notes ([`9b368cb`](https://github.com/datajoint/element-deeplabcut/commit/9b368cb1ec7a6fb37ed9ee5b0a8fed0a78139ae5))

* Refactor readme, remove images, add docker. See details

Docker: add dev and test environments/dockerfiles
changelog/version.py: revise version number
remove images: lab, session, subject diagrams
README: refactor with links to images. Direct to central install.md for instructions
1_Explore_Workflow: update to show new functionality
requirements: pinn versions
tests: Minor edits to supress linter errors
user_data: move config parameters to new csv
ingest: update for config parameters
paths.py: update for cross-element consistency
pipeline.py: Minor edits to supress linter errors ([`3494447`](https://github.com/datajoint/element-deeplabcut/commit/3494447ad249a21a90fdfbf5b1ba0fda970222a3))

* new dev branch ([`87a1f49`](https://github.com/datajoint/element-deeplabcut/commit/87a1f4994868ab3a3234c32e6f6c9a9f1e600d66))

* minor: remove debug notebook cell ([`a580a4c`](https://github.com/datajoint/element-deeplabcut/commit/a580a4c1b201123c3fe4d911d8ef087172a0d933))

* Example ingestion in notebook 01 ([`8350d39`](https://github.com/datajoint/element-deeplabcut/commit/8350d396e9116efc0fabc6d15463799e9620b066))

* repo standard items - changelog, contrib ([`eb3ba17`](https://github.com/datajoint/element-deeplabcut/commit/eb3ba17bfed30abde0b0aba0361c63ec02828502))

* remove ds_stores ([`5550ed8`](https://github.com/datajoint/element-deeplabcut/commit/5550ed8be2fecf31d3d04275f56057dc0be278b2))

* Delete .DS_Store ([`4ddf02f`](https://github.com/datajoint/element-deeplabcut/commit/4ddf02f8ce660c17fec30379957bc5f8bedd6bf3))

* delete notes file ([`aa01866`](https://github.com/datajoint/element-deeplabcut/commit/aa01866417b8757deb6b86d77945809f65b35aa5))

* Initial structure ([`1f324c1`](https://github.com/datajoint/element-deeplabcut/commit/1f324c1e588f07caa33e1b4a7aefe84ca35be536))

* add gitignore ([`cfac635`](https://github.com/datajoint/element-deeplabcut/commit/cfac635e7f07009fe10d800653c4c4bbd36858d6))

* Create README.md ([`94546b1`](https://github.com/datajoint/element-deeplabcut/commit/94546b17b708874ef4536179a2c2bca29cd1cd24))

* [WIP] Update project path in pose config ([`4afc063`](https://github.com/datajoint/element-deeplabcut/commit/4afc06385d47af7d23c76d9761685007c17d0ad3))

* paths,pipeline moved; train and dlc_reader modif ([`b566184`](https://github.com/datajoint/element-deeplabcut/commit/b5661841e836605be99adce91dcc57ae8138026f))

* Merge pull request #80 from kabilar/main

Add DeepLabCut, NWB, and DANDI citations ([`4046d89`](https://github.com/datajoint/element-deeplabcut/commit/4046d89e5508e980ace1e174f7de470b8450281c))

* Add NWB and DANDI citations ([`26922a4`](https://github.com/datajoint/element-deeplabcut/commit/26922a4c7c26aa96f1c950352b11e8c554fec4c9))

* Update changelog ([`e3d2bd9`](https://github.com/datajoint/element-deeplabcut/commit/e3d2bd998b14fcc31e1ddd85d4221178ff307a15))

* Update citation page ([`4293562`](https://github.com/datajoint/element-deeplabcut/commit/4293562ca4a798755d1be02465de21a3cf706e0c))

* Update citation page ([`26deff5`](https://github.com/datajoint/element-deeplabcut/commit/26deff520ab727208ebc7eefd45345e0545a5194))

* Add DeepLabCut citation ([`70e2e3e`](https://github.com/datajoint/element-deeplabcut/commit/70e2e3e52975748f3d4edca7265831e359266d19))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut into main ([`72efe3e`](https://github.com/datajoint/element-deeplabcut/commit/72efe3e0d92ad34ed48eaff9075fd9dfaf7e6b29))

* Merge pull request #79 from kushalbakshi/main

Fix dark mode and CI/CD issues ([`5f8a327`](https://github.com/datajoint/element-deeplabcut/commit/5f8a327bdff7bdd4596d503b2633d8910e8b3570))

## v0.2.5 (2023-05-11)

### Unknown

* Fix dark mode and CI/CD issues ([`bf8bde4`](https://github.com/datajoint/element-deeplabcut/commit/bf8bde4836f93f5950c1548a7251e37ad0d32e97))

* Merge pull request #78 from kushalbakshi/main

Fix docs tutorials in dark mode ([`c91090d`](https://github.com/datajoint/element-deeplabcut/commit/c91090da8ec99a725f6ad3fbb7ffd4b02120e608))

## v0.2.4 (2023-04-28)

### Unknown

* Fix docs tutorials in dark mode ([`3294eaa`](https://github.com/datajoint/element-deeplabcut/commit/3294eaa245dee206c40f2a2a8f2d246a264dd590))

## v0.2.3 (2023-04-05)

### Unknown

* Merge pull request #76 from sidhulyalkar/main

update changelog and version ([`88f9fcf`](https://github.com/datajoint/element-deeplabcut/commit/88f9fcfd7667690a44f2b1a3ed21f56985a058f3))

* update year to 2023 ([`63daae5`](https://github.com/datajoint/element-deeplabcut/commit/63daae521df0f56c210c0ff1e15f0fa99e818316))

* Update CHANGELOG.md

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`bd92c94`](https://github.com/datajoint/element-deeplabcut/commit/bd92c94b8ece385825c6e919fa50f8d996f80bc8))

* update changelog releases ([`a21a471`](https://github.com/datajoint/element-deeplabcut/commit/a21a4715c343db6b8578b4213fe8a4ede5b84caa))

* update changelog and version ([`8f355dd`](https://github.com/datajoint/element-deeplabcut/commit/8f355dd2d393f481bce3588f20a916da7ca41aa8))

* Update docs ([`bde3edb`](https://github.com/datajoint/element-deeplabcut/commit/bde3edb829b2700b95bd06ea08991ff893b7ac68))

* Remove Google Analytics key ([`e6037e0`](https://github.com/datajoint/element-deeplabcut/commit/e6037e0ffb7991b34995a4ea011080138693c1db))

* Remove Google Analytics key ([`c8c72f0`](https://github.com/datajoint/element-deeplabcut/commit/c8c72f0c4b40804728484a13ba4dbe8c0721ff31))

* Merge pull request #75 from ttngu207/main

fix bug ([`40503d7`](https://github.com/datajoint/element-deeplabcut/commit/40503d7b8abbb77c3ffcfba318b1fdf2ca270a10))

* fix bug ([`37a100c`](https://github.com/datajoint/element-deeplabcut/commit/37a100c0c07042cb4fecda355336687d445f8db7))

* Merge pull request #74 from sidhulyalkar/main

DLC bugfix ([`1627433`](https://github.com/datajoint/element-deeplabcut/commit/16274333416abc81b24564ddf3fb715da19a2c2e))

* bugfix, handles case where multiple subjects have the same recording_id ([`92764ae`](https://github.com/datajoint/element-deeplabcut/commit/92764ae840930d460e7151a8c8a1fcac2125b37b))

* revert fixing torch version ([`f5448f3`](https://github.com/datajoint/element-deeplabcut/commit/f5448f316561339f4cfe0ea1b3a7c3eb148aeece))

* fix torch version in reqs ([`fda1ecb`](https://github.com/datajoint/element-deeplabcut/commit/fda1ecb150e4b1fa80b5872323d8c753755a1046))

* Merge branch &#39;main&#39; of https://github.com/sidhulyalkar/element-deeplabcut ([`9a3001d`](https://github.com/datajoint/element-deeplabcut/commit/9a3001d301a5768b80f349ce1b6f5025f92ac80d))

* Merge pull request #73 from CBroz1/main

Add interface to requirements ([`1b78339`](https://github.com/datajoint/element-deeplabcut/commit/1b783396a2d11aaca6817abcee0384d917bdf30b))

* Merge branch &#39;main&#39; into main ([`5201430`](https://github.com/datajoint/element-deeplabcut/commit/5201430d84587760502a08ccd6e480428e091929))

* Add interface to requirements ([`63af644`](https://github.com/datajoint/element-deeplabcut/commit/63af64408d5efc574aa18f9934a8d265844661ac))

* fix torch version ([`5f8594c`](https://github.com/datajoint/element-deeplabcut/commit/5f8594c054851ed62f32b7e4ecebbcb343233497))

## v0.2.2 (2023-01-17)

### Unknown

* Merge pull request #72 from sidhulyalkar/main

Move Rest of DLC imports into make functions ([`802eb0a`](https://github.com/datajoint/element-deeplabcut/commit/802eb0a243f5b2f87ce510931c09625c38efdcc0))

* Update CHANGELOG.md

Co-authored-by: Chris Brozdowski &lt;CBrozdowski@yahoo.com&gt; ([`44607f2`](https://github.com/datajoint/element-deeplabcut/commit/44607f21cc16354e5ef408e8c765919fbf74211f))

* update changelog and version ([`65cd9cf`](https://github.com/datajoint/element-deeplabcut/commit/65cd9cfbbea283c704bf196dbbaf91af10a77e5a))

* add isort:skip to moved imports ([`88a402d`](https://github.com/datajoint/element-deeplabcut/commit/88a402df76809b908d5da3932532fbdc92bc6a84))

* move DLC imports into make functions where they are used ([`2654b7d`](https://github.com/datajoint/element-deeplabcut/commit/2654b7d08ba79c77f9201d045b142f81d4f6936a))

* Merge pull request #71 from sidhulyalkar/main

Move evaluate_network import into make function in model.py ([`bee89bf`](https://github.com/datajoint/element-deeplabcut/commit/bee89bfb4e4553795585e3564ed5bf52e552697c))

* Merge branch &#39;datajoint:main&#39; into main ([`2f2a9a1`](https://github.com/datajoint/element-deeplabcut/commit/2f2a9a14c4b09e137ed68bb547ae0cf0ef8705e7))

* Merge pull request #70 from sidhulyalkar/main

Move import into make function ([`3f83619`](https://github.com/datajoint/element-deeplabcut/commit/3f83619478f0ef6225f32a2261f6ae4bf8519435))

* Merge branch &#39;main&#39; of https://github.com/sidhulyalkar/element-deeplabcut ([`f3a6f29`](https://github.com/datajoint/element-deeplabcut/commit/f3a6f29c7bc891fb5d37134b613f6e491d5f3f13))

* Update element_deeplabcut/train.py

Add # isort:skip to moved import

Co-authored-by: Chris Brozdowski &lt;CBrozdowski@yahoo.com&gt; ([`aeb8808`](https://github.com/datajoint/element-deeplabcut/commit/aeb8808042f58da1e4566c4e30a84c3a4908049c))

* move evaluate_network import into make function ([`25d6524`](https://github.com/datajoint/element-deeplabcut/commit/25d6524c6ad9ea164654198049f5ffd36a498729))

* Merge branch &#39;datajoint:main&#39; into main ([`3d54566`](https://github.com/datajoint/element-deeplabcut/commit/3d54566bde85aa6afd15febef4b7c1ace57782f1))

* Merge pull request #69 from ttngu207/main

improve &#34;insert_estimation_task&#34;; loading DLC results handles multiple DLC output files ([`cb2b4cd`](https://github.com/datajoint/element-deeplabcut/commit/cb2b4cd66a35248e6af6d5d2a98d78f8d9eec661))

* Apply suggestions from code review

Co-authored-by: Chris Brozdowski &lt;CBrozdowski@yahoo.com&gt; ([`a3a70bc`](https://github.com/datajoint/element-deeplabcut/commit/a3a70bc9cddb003c893ad1e992640513f2e2703b))

* raise FileNotFound error instead of Assertion error ([`7b990c7`](https://github.com/datajoint/element-deeplabcut/commit/7b990c71985b86ec8cd111ee97f7a52a3c135b91))

* bugfix - address PR comments ([`ef69e6c`](https://github.com/datajoint/element-deeplabcut/commit/ef69e6c34cb5cf7f1c865afc304254634bb5f0e2))

*  `insert_estimation_task` as alias for `generate` ([`f1ea3f9`](https://github.com/datajoint/element-deeplabcut/commit/f1ea3f9df0052b8c972de238bcabe18adcd1d16e))

* Update CHANGELOG.md ([`1391f7a`](https://github.com/datajoint/element-deeplabcut/commit/1391f7a1fd88dfcacc6b69cbdbdd56e768b595e6))

* DLC reader allowing for loading dlc output in multi-file format ([`486fdaf`](https://github.com/datajoint/element-deeplabcut/commit/486fdaf8765112b713fd0dab5639a20085f788fa))

* improve &#34;insert_estimation_task&#34;, renamed to &#34;generate&#34; ([`7d15fbe`](https://github.com/datajoint/element-deeplabcut/commit/7d15fbe82216474a53eea705c8233a7bb4661d9b))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut ([`7ce878a`](https://github.com/datajoint/element-deeplabcut/commit/7ce878aa08b9fbc8fde311c7bb32d2fa438a9345))

* code cleanup ([`2dce4a0`](https://github.com/datajoint/element-deeplabcut/commit/2dce4a0632ddc30b3cba7cc5637db5a1e96c0e80))

* clean up - grouping of &#34;trigger&#34; specific steps ([`0c9cc13`](https://github.com/datajoint/element-deeplabcut/commit/0c9cc13290103a1b7750655899ec271555aedbb1))

* move train_network import into make function where it is used ([`e8fe0d7`](https://github.com/datajoint/element-deeplabcut/commit/e8fe0d79d864e2cbc78f117fcda5c15469dbe820))

* Merge pull request #68 from kabilar/main

Update tutorial page ([`13cc3ea`](https://github.com/datajoint/element-deeplabcut/commit/13cc3ea49c7fd0b6b35056814fefd1a4d62438a4))

* Update tutorial page ([`8e2f75e`](https://github.com/datajoint/element-deeplabcut/commit/8e2f75eb8ae7da3fdf544d54c0c3686913b6c467))

## v0.2.1 (2022-12-16)

### Fix

* fix: 🐛 docs docker issue ([`3a5c5f6`](https://github.com/datajoint/element-deeplabcut/commit/3a5c5f647a94b616134a19d72f5b40041744c0d9))

### Refactor

* refactor(CICD): 🔥 clean up dev CICD for docs ([`f14e9b2`](https://github.com/datajoint/element-deeplabcut/commit/f14e9b2b8b8d17fbd79d1ce344a8f5478c195265))

### Test

* test(CICD): 🧪 4 ([`fcb3d3e`](https://github.com/datajoint/element-deeplabcut/commit/fcb3d3e949b05eca0c5c7e5d11717d2fdf2b845a))

* test(CICD): 🧪 3 ([`ec7f00b`](https://github.com/datajoint/element-deeplabcut/commit/ec7f00b61f9602fe89fa546886d564f36e21abd1))

* test(CICD): 🧪 2 ([`dcf22f6`](https://github.com/datajoint/element-deeplabcut/commit/dcf22f6e97079fcbf6e711665f9324de18eb290a))

* test(CICD): 🧪 1 ([`8c92443`](https://github.com/datajoint/element-deeplabcut/commit/8c924431a98435e8e36dc405a7dd984b1011c3b8))

### Unknown

* Merge pull request #67 from sidhulyalkar/main

Fix requirements for DLC setting tensorflow to be a subpackage ([`7fe2ad6`](https://github.com/datajoint/element-deeplabcut/commit/7fe2ad69e8959e1f5afc8eac82041ffc4c6c184d))

* Update CHANGELOG.md

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`49f51af`](https://github.com/datajoint/element-deeplabcut/commit/49f51af5de55eac91f32f186ea459c323dd035d6))

* Update element_deeplabcut/version.py

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`1fc8949`](https://github.com/datajoint/element-deeplabcut/commit/1fc8949f5e430583d3ca31bbc1b1db67c6b9fa29))

* fixed markdown linting ([`82762ee`](https://github.com/datajoint/element-deeplabcut/commit/82762eecaa26f338f597906403c9924508452a90))

* remove space ([`93b626b`](https://github.com/datajoint/element-deeplabcut/commit/93b626bd8e9d4ccf1b589a1d240abeb904ea13e8))

* update changelog ([`f75aba0`](https://github.com/datajoint/element-deeplabcut/commit/f75aba0ed130cec084ef330afe6311945480f3c0))

* updated version to 0.2.2 ([`618a63d`](https://github.com/datajoint/element-deeplabcut/commit/618a63d33bce16adcac18e3341852e2329e70b10))

* remove space ([`22fbefa`](https://github.com/datajoint/element-deeplabcut/commit/22fbefa88213d83a3dbab30b77b94d74793ea982))

* Fixed requirements to handle DLC package change, fixed typo in docstring ([`54d2307`](https://github.com/datajoint/element-deeplabcut/commit/54d2307aa0bb4eb515905276e33617634a1c38fc))

* Merge pull request #66 from CBroz1/main

[bugfix] Render notebooks as tutorials ([`e8fc1da`](https://github.com/datajoint/element-deeplabcut/commit/e8fc1dac844ad307777b1d55c52b981f0a77087a))

* uncomment docker compose ([`889f7df`](https://github.com/datajoint/element-deeplabcut/commit/889f7df91b1b5c9ab76b1ec0d272a6a573134e5d))

* 🐛 notebook render bugfix ([`8943325`](https://github.com/datajoint/element-deeplabcut/commit/894332515822408570ff2274e544dc93b12111a3))

* Minor fixes ([`eaecf59`](https://github.com/datajoint/element-deeplabcut/commit/eaecf59a66e50964ec65e8b5b20e1d89245262cd))

* Merge pull request #65 from CBroz1/docs-tutorial

[bugfix] Remove gitignore item for mkdocs notebook deployment ([`5264f2d`](https://github.com/datajoint/element-deeplabcut/commit/5264f2d80d561f5f468d11cae22d6bbafe7cf73c))

* Remove gitignore item for mkdocs notebook deployment ([`a97f998`](https://github.com/datajoint/element-deeplabcut/commit/a97f9980e2842424356f8153a85f8a047e062715))

* Merge pull request #55 from CBroz1/docs-tutorial

Tutorials folder with rendered notebooks ([`c628e32`](https://github.com/datajoint/element-deeplabcut/commit/c628e32b2efc622f9a3d9b25668221c88d850eb6))

* Update docs/src/tutorials/index.md

Co-authored-by: Tolga Dincer &lt;tolgadincer@gmail.com&gt; ([`204436a`](https://github.com/datajoint/element-deeplabcut/commit/204436a71362b6bb622bb4009121cfed32bcc3c3))

* Fetch from cbroz1:main ([`55422b3`](https://github.com/datajoint/element-deeplabcut/commit/55422b37d1e682404a6fabefa8bb110e9385badf))

* Add notebooks to docs; Add markdown linting ([`d306b34`](https://github.com/datajoint/element-deeplabcut/commit/d306b345b98c3382b63289b2ec01b6802ade8fd4))

* Merge pull request #64 from kabilar/main

Fix changelog for CICD ([`128f66d`](https://github.com/datajoint/element-deeplabcut/commit/128f66d180519852f4343d961c04e07a412a1af9))

* Fix changelog for CICD ([`dbd8c49`](https://github.com/datajoint/element-deeplabcut/commit/dbd8c49d6988545939c9c06f3d9ef116a606a3b8))

* Merge pull request #63 from kabilar/main

Update styling for docs launch ([`411225b`](https://github.com/datajoint/element-deeplabcut/commit/411225b6f3b57f3e6a7ae2a77554863775827342))

* Update changelog ([`a3a3a5f`](https://github.com/datajoint/element-deeplabcut/commit/a3a3a5f1be5dcec25e4bbbc0e98b740b0413ca40))

* Update social icon colors ([`bd52c5c`](https://github.com/datajoint/element-deeplabcut/commit/bd52c5ca0a2b211396c2a7269a40caaf6a021c71))

* Update format ([`9b77e82`](https://github.com/datajoint/element-deeplabcut/commit/9b77e8285c973d833fb23d0a5ded5ad57e93501e))

* Update logo in yaml ([`d57826e`](https://github.com/datajoint/element-deeplabcut/commit/d57826e543469ec76662a70a46026225081d6b90))

* Update logos ([`dd437cf`](https://github.com/datajoint/element-deeplabcut/commit/dd437cf6bb35e45a774aeba56bfd5f38541cacba))

* Add drawio version ([`c38f187`](https://github.com/datajoint/element-deeplabcut/commit/c38f187c06a0d2ed1925379a50b28dc20b713aaf))

* Update diagram ([`8e74276`](https://github.com/datajoint/element-deeplabcut/commit/8e74276bb2ce1bde9544838e6d9b2325c7b36e47))

* Update diagram ([`40d541c`](https://github.com/datajoint/element-deeplabcut/commit/40d541c1cd63ccbf88af76cd68cb31b904e87253))

* Update text format ([`b721de3`](https://github.com/datajoint/element-deeplabcut/commit/b721de3bb82233312399c4454885c8a8b31f710e))

* Update to transparent background ([`2b66228`](https://github.com/datajoint/element-deeplabcut/commit/2b662284c095f9ee0debdf5ca55b16bedbaed783))

* Add flowchart ([`0d5deae`](https://github.com/datajoint/element-deeplabcut/commit/0d5deae05a88abb28f30d159b6c7f58a6f3e3d01))

* Remove next/previous navigation from footer ([`29291f5`](https://github.com/datajoint/element-deeplabcut/commit/29291f54696980b84647e91d01581d44adf6b0a7))

* Remove google analytics feedback ([`6923912`](https://github.com/datajoint/element-deeplabcut/commit/692391205525a91a016bbd32aa02c508cba8bd6a))

* Merge pull request #62 from CBroz1/main

Fix typos ([`dbb2245`](https://github.com/datajoint/element-deeplabcut/commit/dbb224561dd2e068797f79b754c07f6a6ae33a69))

* Revise docstrings ([`eacf864`](https://github.com/datajoint/element-deeplabcut/commit/eacf864c2203d11b6f33a64407130693dc3f1fb9))

* Merge pull request #60 from sidhulyalkar/main

change nframes from smallint to int data type ([`e07dc77`](https://github.com/datajoint/element-deeplabcut/commit/e07dc77935f9345de6882cec12981d2d23c62a1d))

* change nframes from smallint to int data type ([`f54e054`](https://github.com/datajoint/element-deeplabcut/commit/f54e054014470add4b38db772e6daf76f192f3b8))

* Merge pull request #59 from JaerongA/docs

fix minor typos &amp; data types ([`6bb2861`](https://github.com/datajoint/element-deeplabcut/commit/6bb2861e368252409825de5ed5ff60c9dddcd2ff))

* fix typo &amp; data type in models.py ([`ccdf1ec`](https://github.com/datajoint/element-deeplabcut/commit/ccdf1ec0c9e0c0ff474dd1bf559ba357fbaa941e))

* fixed minor typos ([`04965e2`](https://github.com/datajoint/element-deeplabcut/commit/04965e2054e12d9ae554df52ec151f31fd4995cd))

* fix typos ([`d0a80ca`](https://github.com/datajoint/element-deeplabcut/commit/d0a80ca5f1155881c89e2eb575abb8d5da55ec24))

* Merge pull request #58 from CBroz1/main

Version as env variable ([`0db4ba8`](https://github.com/datajoint/element-deeplabcut/commit/0db4ba8e931e77f8c1df2cde38d49f046e3a362c))

* Render API in source order ([`17af889`](https://github.com/datajoint/element-deeplabcut/commit/17af88935df8a668104b3fc1602531162087765d))

* Fix URL ([`1f9c277`](https://github.com/datajoint/element-deeplabcut/commit/1f9c277126fc86e77ae6b842eb05e15761dd10a0))

* Fix typo ([`11c1a55`](https://github.com/datajoint/element-deeplabcut/commit/11c1a5594d04868171de690b12dc5b421cf870c8))

* Version as env variable ([`352c44f`](https://github.com/datajoint/element-deeplabcut/commit/352c44f98325cb79a249026d84310bff8417e7e2))

* Merge pull request #57 from CBroz1/main

Add 404, chatbot. Remove extra CICD items ([`11b627d`](https://github.com/datajoint/element-deeplabcut/commit/11b627de820125dc82ef0eaac67cecd48ea06bcf))

* Add 404, chatbot. Remove extra CICD items ([`87d541c`](https://github.com/datajoint/element-deeplabcut/commit/87d541c5cb4fc3602ae0b8f616fe2a1f0fb24834))

* Add missing changelog link ([`0dd064a`](https://github.com/datajoint/element-deeplabcut/commit/0dd064aa333cfc38d9da5e2fbe77f3b48a529c40))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut into docs-tutorial ([`4422725`](https://github.com/datajoint/element-deeplabcut/commit/4422725823f263d7c4acf06b8ce36942805bb260))

* Merge pull request #56 from CBroz1/docs

Add docs ([`99894bc`](https://github.com/datajoint/element-deeplabcut/commit/99894bc67e8ff4cf83596de88079b0734a0b0223))

* Element API docs -&gt; https urls ([`b7c5122`](https://github.com/datajoint/element-deeplabcut/commit/b7c5122a4616fc8a79477256bcc4eba5daddffbf))

* Fix links in concepts ([`157d545`](https://github.com/datajoint/element-deeplabcut/commit/157d545eb21b6d83b08656ac39daf30d706c6c77))

* Version bump ([`2d7c588`](https://github.com/datajoint/element-deeplabcut/commit/2d7c588eee1139538d11adac69c23d9f6a2a001a))

* See details.

Readme: add https://
Changelog: remove subheading
docs/mkdocs.yaml: changelog new path, revise contributor notes
docs/src/api/make_pages.py:
    - revert URL to main
    - add logic to exclude __init__.py
docs/src/changelog: move
docs/src/concepts.md:
    - move architecture after features
    - add dlc_session_to_nwb
    - rephrase language for model training
    - hard wrap on pgfs added in code review
docs/src/index.md: add spacing for linebreaks
element_deeplabcut/model and train: Add attributes to docstrings ([`4394572`](https://github.com/datajoint/element-deeplabcut/commit/4394572fbc9cb4cc24403ba4cd8d8cfd441cc252))

* Apply suggestions from code review

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`5436db8`](https://github.com/datajoint/element-deeplabcut/commit/5436db878faf82a7d940c8217f0e3adfa502d584))

* Apply suggestions from code review

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`bc05121`](https://github.com/datajoint/element-deeplabcut/commit/bc05121bc9ffd0e42aab40777ab0965baaf51f70))

* Add full tutorial draft ([`d00a1f7`](https://github.com/datajoint/element-deeplabcut/commit/d00a1f7fe5acf4ccac61f622c32ad91f9b6dbb28))

* Remove Tutorials content, replace with ComingSoon ([`2397f4c`](https://github.com/datajoint/element-deeplabcut/commit/2397f4c2cee54b7fd7f1e1192d7d20682f286a67))

* Concepts.md: Move partnerships above architecture ([`395537e`](https://github.com/datajoint/element-deeplabcut/commit/395537eac06940d2a41495fd4fe03a8b162d2d85))

* Change title on index.md ([`fcc4c0c`](https://github.com/datajoint/element-deeplabcut/commit/fcc4c0c23e4d02181ff56c4a609fb320d1a3a9de))

* Add analytics key to docker compose ([`90682c1`](https://github.com/datajoint/element-deeplabcut/commit/90682c1b0acb478a6254d96494bc1ff7f11085c0))

* Apply suggestions from code review

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`285dfa1`](https://github.com/datajoint/element-deeplabcut/commit/285dfa1faa86e95cb6b6e851f86288a33cea7ad3))

* Add high level descriptions and DLC steps ([`064f721`](https://github.com/datajoint/element-deeplabcut/commit/064f7214ff494f2ae75223dad02c0fa0d3386f31))

* Merge branch &#39;docs2&#39; of https://github.com/CBroz1/element-deeplabcut ([`0a28279`](https://github.com/datajoint/element-deeplabcut/commit/0a282796f9ccfbdfa6fd35f56383e5202ca127b7))

* Citation to own page. Changelog to top level ([`31d834a`](https://github.com/datajoint/element-deeplabcut/commit/31d834a696ed6942d62c20a99f2828fe3b16fd50))

* Merge branch &#39;docs&#39; of https://github.com/CBroz1/element-deeplabcut into docs ([`939abe0`](https://github.com/datajoint/element-deeplabcut/commit/939abe013344201cb8ed62b57c47e5b359e6d18a))

* Update docs/src/tutorials.md

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`7b40fe0`](https://github.com/datajoint/element-deeplabcut/commit/7b40fe07959a7ebc7c1f19e37d82a45546a616a3))

* Apply suggestions from code review

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`f991cbe`](https://github.com/datajoint/element-deeplabcut/commit/f991cbea6d1debd0df2b9474d04dd89dd499ffd4))

* Apply suggestions from code review

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`b410b55`](https://github.com/datajoint/element-deeplabcut/commit/b410b554bf74305c9c8c2744731ba967b95d736f))

* Revert docker compose edits ([`8e36f5b`](https://github.com/datajoint/element-deeplabcut/commit/8e36f5bddb3c94348a64e6d124d3428ee86b6009))

* test with mkdocs instead of mike ([`eac8be4`](https://github.com/datajoint/element-deeplabcut/commit/eac8be426635828b0fd8b07512ee0bb31bc447ad))

* Add global safe config hack ([`14485be`](https://github.com/datajoint/element-deeplabcut/commit/14485be90e05006acce751ef3d24a81c9b401af7))

* Remove workflow-dispatch trigger from mkdocs-build workflow ([`dc90bd1`](https://github.com/datajoint/element-deeplabcut/commit/dc90bd1b56d4b9c8a1eae9f8219aa91801415aee))

* Remove tag check from mkdocs-build ([`4016d49`](https://github.com/datajoint/element-deeplabcut/commit/4016d49ab65a263c8c299f85dffbdd21f47ba9fe))

* Add staging CICD, Add element-generic mkdocs publish ([`bc3fbf0`](https://github.com/datajoint/element-deeplabcut/commit/bc3fbf06a4c4687d8d3ec0166099f70acc3e8d31))

* Mention DANDI upload ([`77a0629`](https://github.com/datajoint/element-deeplabcut/commit/77a06294395ee5f23c3c99a48726ded809f65ffc))

* Add codebook mention. Revise changelog symbolic link ([`6d9125d`](https://github.com/datajoint/element-deeplabcut/commit/6d9125d199d09730b019c12d4047c458312c5a75))

* Add codebook mention to tutorials#notebooks ([`7e0be4e`](https://github.com/datajoint/element-deeplabcut/commit/7e0be4e2764ca4a86a70e01319049d92455339e6))

* Home nav to docs/elements/ ([`0f6f550`](https://github.com/datajoint/element-deeplabcut/commit/0f6f5500c2b9b76fb71940eccfdbe08c2eaa08c0))

* Hard wrap; Concepts#data-export ([`ae75dae`](https://github.com/datajoint/element-deeplabcut/commit/ae75daea87607b5fa6dca27bd9ffe159b771532f))

* Apply suggestions from code review 3

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`7110b72`](https://github.com/datajoint/element-deeplabcut/commit/7110b723f1144daa21c9202f978c19f44e97b4fe))

* Apply suggestions from code review 2

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`9b4ce4d`](https://github.com/datajoint/element-deeplabcut/commit/9b4ce4d9f43c1e2f7891efaf9546f19f708ed66a))

* Apply suggestions from code review

Co-authored-by: Kabilar Gunalan &lt;kabilar@datajoint.com&gt; ([`276526b`](https://github.com/datajoint/element-deeplabcut/commit/276526b03f757742b94c75b8dd689996f8811423))

* Edits to make_pages to handle edge cases ([`c34289a`](https://github.com/datajoint/element-deeplabcut/commit/c34289a4ece95be61e4348db917d2a0892a2c883))

* Misc extra contributor notes ([`061f39f`](https://github.com/datajoint/element-deeplabcut/commit/061f39f0effa494de6f7cdbabd4f53ce5c9a1ee7))

* Revise doc structure ([`4fe5fc0`](https://github.com/datajoint/element-deeplabcut/commit/4fe5fc0f2ed63bb835843f92c77dfc484e27c66c))

* Docstrings -&gt; Google style; edit css style for blue main ([`afd4602`](https://github.com/datajoint/element-deeplabcut/commit/afd4602d42e1e07e32daab8cd3740d36e40d4c0f))

* Merge pull request #10 from guzman-raphael/docs

Include workflow API docs ([`6fff4ab`](https://github.com/datajoint/element-deeplabcut/commit/6fff4ab80c3f175daf6ad2bff88a24fdbba60a8b))

* Include workflow API if applicable. ([`6ca812a`](https://github.com/datajoint/element-deeplabcut/commit/6ca812a9aed85f68a3171ce8d0ddfd28eddf0d8c))

* Fix merge conflicts. ([`b511e8e`](https://github.com/datajoint/element-deeplabcut/commit/b511e8e4c7718b680a0fae251904b013fde0bf2e))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut into docs ([`116fd90`](https://github.com/datajoint/element-deeplabcut/commit/116fd90e1588bbeec78a08e822680ece6ea5abb6))

* WIP: update docs to include workflow API docs ([`dece185`](https://github.com/datajoint/element-deeplabcut/commit/dece1854c5fd572f5f4243d82ed704894d121a1e))

* Add docs ([`081d3f7`](https://github.com/datajoint/element-deeplabcut/commit/081d3f76bb83e797838f0b1ff623fd8e3213eb96))

## v0.2.0 (2022-10-10)

### Feature

* feat(CICD): ♻️ clean up old CICD, deploy update in Prod ([`35310a9`](https://github.com/datajoint/element-deeplabcut/commit/35310a92c1645dca469aacb8a87701f78cbe804e))

* feat(CICD): ✨ calling reusable context check ([`ce8409d`](https://github.com/datajoint/element-deeplabcut/commit/ce8409dc4db21f5c3cece789497c3b1571a80fbb))

* feat(CICD): ✨ use workflow_run ([`22d0959`](https://github.com/datajoint/element-deeplabcut/commit/22d0959ee39d0523b5d93b5d8201e60b4e618696))

### Fix

* fix(CICD): 🐛 CICD trigger fixed ([`4bd38ac`](https://github.com/datajoint/element-deeplabcut/commit/4bd38ace25c40bffebc098a14eb0f0ae04057ab3))

* fix(CICD): 🐛 before_release workflow not triggerred by push with tag ([`90e7d6c`](https://github.com/datajoint/element-deeplabcut/commit/90e7d6c13b31db81f348a7b6d128cdec24146aeb))

* fix(CICD): 🐛 trigger logic update ([`b4970e6`](https://github.com/datajoint/element-deeplabcut/commit/b4970e6f1ed472b221c66f3e7514923fbbeb0abb))

* fix(CICD): 🐛 fix context_check ref ([`6ba53de`](https://github.com/datajoint/element-deeplabcut/commit/6ba53def3051ae0ffb2268fd4f112e25ce939fa9))

* fix(CICD): ✨ pause auto trigger old CI ([`94b0b92`](https://github.com/datajoint/element-deeplabcut/commit/94b0b92578d89d1044935559b0aee6745fce3729))

* fix(CICD): 🐛 missing py_ver input ([`f2d3bf3`](https://github.com/datajoint/element-deeplabcut/commit/f2d3bf33907e5d512a3a8701d8294f4c9ac855d0))

* fix(CICD): 🐛 multiline ([`7ac7cbb`](https://github.com/datajoint/element-deeplabcut/commit/7ac7cbb85c319d1ace894932fffc75637505efc2))

* fix(CICD): 🐛 typo ([`04f2d7e`](https://github.com/datajoint/element-deeplabcut/commit/04f2d7ea06a3d1d91f37b0afcd7ddeb466a7d451))

* fix(CICD): 🐛 if syntax ([`47fc868`](https://github.com/datajoint/element-deeplabcut/commit/47fc868b6643bc035bf9f3df66f45e573444a9a1))

* fix(CICD): 🧪 test release ci ([`f0a4dc8`](https://github.com/datajoint/element-deeplabcut/commit/f0a4dc8cb3a455b7d6b0849304cdfa65edeb7fbb))

* fix(CICD): 🐛 if syntax ([`a4568b6`](https://github.com/datajoint/element-deeplabcut/commit/a4568b6767585876e09058e71aed43f6def09f00))

* fix(CICD): 🐛 fix inputs ([`28a2203`](https://github.com/datajoint/element-deeplabcut/commit/28a2203679f35f826bbe6c7e7aac1e8f4f21dafb))

* fix(CICD): 🐛 update logic ([`70c2bab`](https://github.com/datajoint/element-deeplabcut/commit/70c2bab581520a232b79ca2e443e7bd2c53b1a22))

* fix(CICD): 🐛 update reference ([`9c4dcaf`](https://github.com/datajoint/element-deeplabcut/commit/9c4dcaf8b850ea6e5ced7d74f8960eb76151ff49))

* fix(CICD): 🐛 simplify logic ([`6b3d2e7`](https://github.com/datajoint/element-deeplabcut/commit/6b3d2e7c5e190a96ebb9929738b3a2300037e32c))

* fix(CICD): 🐛 trigger ([`629022a`](https://github.com/datajoint/element-deeplabcut/commit/629022aa2a153bb9ce0d6a0c44c68389b3762d0e))

* fix(CICD): 🐛 typo ([`e2cb051`](https://github.com/datajoint/element-deeplabcut/commit/e2cb051044d9e990c8c47ba1385dca05d1f52d1c))

### Test

* test(CICD): 🧪 7 ([`8b7c98c`](https://github.com/datajoint/element-deeplabcut/commit/8b7c98ca29b67a185944d7cd68c7b9c1230568ab))

* test(CICD): 🧪 6 ([`c3d8b46`](https://github.com/datajoint/element-deeplabcut/commit/c3d8b465a1a43605f2cbcd81f960a3e019dccdff))

* test(CICD): 🧪 5 ([`3ffc527`](https://github.com/datajoint/element-deeplabcut/commit/3ffc527fa851eb94fbc4c24049ee3f65ddeeebf8))

* test(CICD): 🧪 4 ([`69f3a7e`](https://github.com/datajoint/element-deeplabcut/commit/69f3a7e2f9dcb1a4f3c8e98d5ef33d3a080fcd11))

* test(CICD): 🧪 3 ([`14d4422`](https://github.com/datajoint/element-deeplabcut/commit/14d44222127132bc612488b0af0e0d3e511e0437))

* test(CICD): 🧪 2 ([`b3bd687`](https://github.com/datajoint/element-deeplabcut/commit/b3bd687db34acb196b80f5039a9693fb76496fb6))

* test(CICD): 🧪 1 ([`60dffd5`](https://github.com/datajoint/element-deeplabcut/commit/60dffd5ac417ff4cd3d8b0d93f38e4ddd4ff9296))

* test(CICD): 🧪 13 ([`83f71a4`](https://github.com/datajoint/element-deeplabcut/commit/83f71a4752932a95df3f3b41f8b13b67d3c2a32f))

* test(CICD): 🧪 test flow ([`d63d324`](https://github.com/datajoint/element-deeplabcut/commit/d63d324ee30d99ec228cb5dd01fd8c8a98b36b71))

* test(CICD): ✅ 12 ([`dbbb9e5`](https://github.com/datajoint/element-deeplabcut/commit/dbbb9e57e344c1c250db7948e280d1ed03587e37))

* test(CICD): 🧪 11 ([`1053789`](https://github.com/datajoint/element-deeplabcut/commit/105378945c2fbe110d1e8ea39d12b7aea84979f1))

* test(CICD): 🧪 10 ([`154ed9d`](https://github.com/datajoint/element-deeplabcut/commit/154ed9d319692c7d7c26a377185b31644ad7d9b5))

* test(CICD): 🧪 9 ([`591b727`](https://github.com/datajoint/element-deeplabcut/commit/591b72728593e8af5c483b848b23a739356670ac))

* test(CICD): 🧪 8 ([`bd2be1d`](https://github.com/datajoint/element-deeplabcut/commit/bd2be1d060395eabb7b5de709d614549c4ecaa57))

* test(CICD): 🧪 7 ([`360a26c`](https://github.com/datajoint/element-deeplabcut/commit/360a26c4a0b4c1378451327888b4ec343d66dad4))

* test(CICD): 🧪 6 ([`756dfd0`](https://github.com/datajoint/element-deeplabcut/commit/756dfd0e3283623525a0698dae605169d5683ecb))

* test(CICD): 🧪 5 ([`ff94425`](https://github.com/datajoint/element-deeplabcut/commit/ff94425c919b934d656b7545fc69908b89767f96))

* test(CICD): 🧪 4 ([`e321684`](https://github.com/datajoint/element-deeplabcut/commit/e321684ef4954914522891ead371084c62734eb5))

* test(CICD): 🧪 3 ([`ed1e50b`](https://github.com/datajoint/element-deeplabcut/commit/ed1e50b1a83f3f0f9f928baba41b81215ee14d7b))

* test(CICD): 🧪 2 ([`cf3ad74`](https://github.com/datajoint/element-deeplabcut/commit/cf3ad74ea0a11c7a7ffd2e83c7cb6f86292703cc))

* test(CICD): 🧪 1 ([`5952918`](https://github.com/datajoint/element-deeplabcut/commit/59529183539864031a265473361ba0fcd55bc9b6))

* test(CICD): 🧪 test ([`65d2f28`](https://github.com/datajoint/element-deeplabcut/commit/65d2f2885cc98c3f565d92eeb25df2bd4f1930f2))

### Unknown

* Merge pull request #54 from CBroz1/main

Prep for pypi publish ([`1fa6984`](https://github.com/datajoint/element-deeplabcut/commit/1fa69844c5b87e36d43939ba2e9bfbc1da5a7f5e))

* Prep for pypi publish ([`346e164`](https://github.com/datajoint/element-deeplabcut/commit/346e164295f8c2f765c7585ae8ad3e5d99d488a0))

* Merge pull request #46 from CBroz1/dev

Add NWB export function ([`d2e4286`](https://github.com/datajoint/element-deeplabcut/commit/d2e4286512df21b66b0c2b5c1e5fd2c82881d6a5))

* Update element_deeplabcut/export/nwb.py ([`b9580de`](https://github.com/datajoint/element-deeplabcut/commit/b9580de6a4418738a1c2b8b06f50302e7ece5a77))

* Update element_deeplabcut/export/nwb.py

Co-authored-by: Tolga Dincer &lt;tolgadincer@gmail.com&gt; ([`a8acb6b`](https://github.com/datajoint/element-deeplabcut/commit/a8acb6b6f16c37bf77e15c68d536324d5db5e862))

* Apply suggestion from code review

Co-authored-by: Dimitri Yatsenko &lt;dimitri@datajoint.com&gt; ([`e65f14f`](https://github.com/datajoint/element-deeplabcut/commit/e65f14ff125cbc2d7c14d4bec35e6414fe4a450d))

* Add logging via datajoint ([`5ff9624`](https://github.com/datajoint/element-deeplabcut/commit/5ff962419a60000bec1bd7cfb181ab9a51be0019))

* Remove unnecessary import ([`8057632`](https://github.com/datajoint/element-deeplabcut/commit/8057632fd00d9860fdd3b4d91cffa3554f396e0d))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut into dev ([`424becb`](https://github.com/datajoint/element-deeplabcut/commit/424becb2daad30975737ad6b7b3733fe73c59ce7))

* Refactor based on DLC2NWB#10 ([`6121e70`](https://github.com/datajoint/element-deeplabcut/commit/6121e707c103765b60f708d421c1610547e50203))

* WIP: add NWB export ([`efaf34a`](https://github.com/datajoint/element-deeplabcut/commit/efaf34a3868da243ab6fadc3c356a5aa381b119b))

* Merge pull request #52 from tdincer/main

add opencv-python-headless in requirements ([`2143d20`](https://github.com/datajoint/element-deeplabcut/commit/2143d203decbc8247ee9f164658d5e108b34c877))

* add opencv-python-headless in requirements ([`6624728`](https://github.com/datajoint/element-deeplabcut/commit/662472892a87e4cca1b7ee37331625cb995be97f))

* Merge pull request #51 from tdincer/main

bug fix: missing f for formatted string ([`cf08e3e`](https://github.com/datajoint/element-deeplabcut/commit/cf08e3e3159fc0be5212f1d2367851fa495e8f3d))

* add log ([`172a4e3`](https://github.com/datajoint/element-deeplabcut/commit/172a4e3c8594a03914cbdd31439bdd7b8a9fba45))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut ([`44ec30e`](https://github.com/datajoint/element-deeplabcut/commit/44ec30eebefcecd96bc445ec00169bc92a5a60f7))

* Merge pull request #50 from tdincer/main

relocate imports ([`2d96b92`](https://github.com/datajoint/element-deeplabcut/commit/2d96b926ecafe02947d3370d73dd6b139b602f3b))

* Update CHANGELOG.md

Co-authored-by: Chris Brozdowski &lt;CBrozdowski@yahoo.com&gt; ([`ddb32b1`](https://github.com/datajoint/element-deeplabcut/commit/ddb32b12286214cfb0bc55872c3df5e0a7ecaad5))

* Update element_deeplabcut/version.py

Co-authored-by: Chris Brozdowski &lt;CBrozdowski@yahoo.com&gt; ([`009fcc8`](https://github.com/datajoint/element-deeplabcut/commit/009fcc8bec086d241bd916f7f8ba92a4cbaf2fbd))

* bug fix: missing f for formatted string ([`68be599`](https://github.com/datajoint/element-deeplabcut/commit/68be599804436685ffb53592d4d60a784de10e98))

* relocate module imports to the top of the file ([`bfd8624`](https://github.com/datajoint/element-deeplabcut/commit/bfd8624f0de96158147926cfa7d18ecb038a6513))

* relocate imports ([`82a5a79`](https://github.com/datajoint/element-deeplabcut/commit/82a5a792882e592f40aac545e16cfc88e5570240))

* Merge pull request #49 from tdincer/main

Decrease model_description char length ([`96c2a9b`](https://github.com/datajoint/element-deeplabcut/commit/96c2a9b71898fefd0509b9a55951e94f0448fcd1))

* model_description size change ([`50438cb`](https://github.com/datajoint/element-deeplabcut/commit/50438cb2f942cee365555450a8deadca44d31abd))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut ([`d527fcb`](https://github.com/datajoint/element-deeplabcut/commit/d527fcb5a8c1f12ea343f2d3575fdd99009be0b6))

* Merge pull request #48 from tdincer/main

Increase model description attr&#39;s size ([`3acc964`](https://github.com/datajoint/element-deeplabcut/commit/3acc96495e9d8e7a8fbb534dc90f55bc41ee6ed1))

* adjust model_description char length ([`58af1ed`](https://github.com/datajoint/element-deeplabcut/commit/58af1ed15632e0c29531e8d9683a11ef1e261c2f))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut ([`a08bbac`](https://github.com/datajoint/element-deeplabcut/commit/a08bbacd93f0b71409f981cdf68167fb92ea2fc2))

* Merge pull request #47 from yambottle/main

fix(CICD): 🐛 CICD trigger fixed ([`02a57f8`](https://github.com/datajoint/element-deeplabcut/commit/02a57f8627d10b97ad4d577a7060dfa63b24339a))

* fix conflict ([`7219118`](https://github.com/datajoint/element-deeplabcut/commit/72191188e07cea6c1a6985b7bb9ea6af43139af1))

* Merge pull request #40 from CBroz1/main

Changes to parallel workflow integration tests ([`8a63b19`](https://github.com/datajoint/element-deeplabcut/commit/8a63b196869a194e1a27ee76e3d4dd6da5de87dd))

* Merge branch &#39;main&#39; of https://github.com/CBroz1/element-deeplabcut ([`1db662b`](https://github.com/datajoint/element-deeplabcut/commit/1db662bbf364a170ddaf42be1d58732f1efc68b8))

* Merge pull request #8 from yambottle/main

Include updated CICD ([`fabbb75`](https://github.com/datajoint/element-deeplabcut/commit/fabbb757e017e841bfd19460fac032aea20ee861))

* Fetch upstream ([`ddca6f6`](https://github.com/datajoint/element-deeplabcut/commit/ddca6f68376faee34d89b081300fc8702fb67d5e))

* Merge branch &#39;main&#39; of https://github.com/CBroz1/element-deeplabcut ([`980cdcb`](https://github.com/datajoint/element-deeplabcut/commit/980cdcb84c5568e6a35d50efa3e76c326a96471a))

* WIP: revise saved config to preserve original video_set ([`271b003`](https://github.com/datajoint/element-deeplabcut/commit/271b00355352ae296c91166743c8ba3337405666))

* fix conflict ([`443548f`](https://github.com/datajoint/element-deeplabcut/commit/443548f3959965bcee2f7e4c5e7c4bb0b425477d))

* Merge branch &#39;chris-main&#39; ([`6283959`](https://github.com/datajoint/element-deeplabcut/commit/628395919278412c14f73c4facf77d1f1dd97923))

* Apply suggestions from code review

Co-authored-by: Tolga Dincer &lt;tolgadincer@gmail.com&gt; ([`8e1f72c`](https://github.com/datajoint/element-deeplabcut/commit/8e1f72c2bc4da617270e7b4e4a7f711ecdce333f))

* Merge branch &#39;main&#39; into main ([`5a7a3e4`](https://github.com/datajoint/element-deeplabcut/commit/5a7a3e437b5ee6a8cfa624bef51a378ba4989039))

* Version bump ([`4bbb209`](https://github.com/datajoint/element-deeplabcut/commit/4bbb20986eab9d7d5a90102c0b1f4ea8a3eba893))

* WIP #36 ([`6f193c1`](https://github.com/datajoint/element-deeplabcut/commit/6f193c1e8e344ccbf7d6f8b779e4fae8de076c9d))

* WIP: pin DLC version, rename saved yaml ([`b4cfe57`](https://github.com/datajoint/element-deeplabcut/commit/b4cfe57829ac6c540e39d1418b10a1dcee3bcca4))

* Apply suggestions from code review

Co-authored-by: Dimitri Yatsenko &lt;dimitri@datajoint.com&gt; ([`bf62231`](https://github.com/datajoint/element-deeplabcut/commit/bf62231a036decc1457216d83355091dee0e7d90))

* WIP: minor fix for save_yaml, permit file ext ([`f1b9b2d`](https://github.com/datajoint/element-deeplabcut/commit/f1b9b2d66db3d04b270507097cc8e82b50a32a61))

* WIP: revert videotype, see DeepLabCut #1900 ([`1fe2fd6`](https://github.com/datajoint/element-deeplabcut/commit/1fe2fd6910277b21701f64ad9c59648846d6289f))

* WIP: error workaround for analyze_videos videotypes param ([`614f02b`](https://github.com/datajoint/element-deeplabcut/commit/614f02b0869141ee2331de426c68ba2950d7219f))

* WIP: change config pointers to our fully managed dict ([`425714d`](https://github.com/datajoint/element-deeplabcut/commit/425714dca54d5071afc297c284457e66c7d20fab))

* WIP: minor bugfixes to output_dir and trainingsetindex as int ([`e630454`](https://github.com/datajoint/element-deeplabcut/commit/e63045453b3a1d70bd647ddfbcb46b696c8aa54b))

* WIP: #24, #26, #27 ([`8e58549`](https://github.com/datajoint/element-deeplabcut/commit/8e58549d98b434c5dfbebc11fc4bb5eebb8bf16f))

* increase model_description char ([`2af9d74`](https://github.com/datajoint/element-deeplabcut/commit/2af9d74377dff0be9fc90c6692d8479e7df043b7))

* Merge pull request #43 from tdincer/main

fix videotype ([`631d7d5`](https://github.com/datajoint/element-deeplabcut/commit/631d7d5fc76cba438dba4853c4b631884fce2d64))

* Update requirements.txt

Co-authored-by: Chris Brozdowski &lt;CBrozdowski@yahoo.com&gt; ([`68134cf`](https://github.com/datajoint/element-deeplabcut/commit/68134cf447fd20a3a83f3feb19b7b84c1abce67a))

* videotype fix ([`d867b7d`](https://github.com/datajoint/element-deeplabcut/commit/d867b7df9f62ec27e00f22591b6f99871094cfdc))

* videotype fix ([`46adbb8`](https://github.com/datajoint/element-deeplabcut/commit/46adbb8b52d8bf39abfec8735e4c47c8701e8c05))

* freeze version ([`c1753c1`](https://github.com/datajoint/element-deeplabcut/commit/c1753c17d2f7b5e7d53256a59d82afbe79ec6cc8))

* revert ([`0d044e2`](https://github.com/datajoint/element-deeplabcut/commit/0d044e2925e3c2d991ebbec0969700be0e9c93e3))

## v0.1.1 (2022-07-06)

### Documentation

* docs: 🐛 changelog remove unreleased and &#39;v&#39; in the tag ([`e194858`](https://github.com/datajoint/element-deeplabcut/commit/e194858edc11f0914da972a6306f10dcea1ec0c5))

* docs(CICD): 🔖 ([`cc95c5b`](https://github.com/datajoint/element-deeplabcut/commit/cc95c5baaf05f5472d8f1f1ff4f2511f0e8a601a))

### Feature

* feat(CICD): 🔖 call reusable cicd with test release ([`32d01ca`](https://github.com/datajoint/element-deeplabcut/commit/32d01ca6a04cb0d160bb4bb323b45d2620e4c62c))

* feat(CICD): ✨ add pypi ([`db5fdd8`](https://github.com/datajoint/element-deeplabcut/commit/db5fdd85a286310058ca5c32484ba59ecd2c7e42))

* feat(CICD): 🔖 point to prod CI ([`d6b2aa3`](https://github.com/datajoint/element-deeplabcut/commit/d6b2aa3b42f2886cc52fc2bb0dc9d230027c62a2))

* feat(CICD): ✨ include debian image build ([`6ba5e73`](https://github.com/datajoint/element-deeplabcut/commit/6ba5e73f23e405c1eeb69a6747db475d17533866))

* feat(CICD): ✨ refer centralized Dockerfile and docker-compose-build.yaml ([`c685dc4`](https://github.com/datajoint/element-deeplabcut/commit/c685dc466bedd31b923ef6d18b84d1c1679a7988))

* feat(CICD): 🐛 add build docker-compose yaml ([`103252f`](https://github.com/datajoint/element-deeplabcut/commit/103252f32c7ad5f20163c4b05ddb1126049e903c))

* feat(CICD): ✨ calling reusable workflow ([`c7152b0`](https://github.com/datajoint/element-deeplabcut/commit/c7152b0775217eea7156253e254a0f03ec735fb4))

### Fix

* fix(CICD): 🐛 have to pass secrets in ([`7ac4d79`](https://github.com/datajoint/element-deeplabcut/commit/7ac4d79c106b08c8bdaabb69625f67a161d8928e))

* fix(CICD): 🐛 only one call is needed, otherwise conflict when create release ([`79223cd`](https://github.com/datajoint/element-deeplabcut/commit/79223cd68f4fd6ec876cb67b8fcceea1c71a6c52))

* fix(CICD): 🐛 fix typo ([`e7fde40`](https://github.com/datajoint/element-deeplabcut/commit/e7fde407bef0b3475e47bafa47a6d083c69c3fd2))

* fix(CICD): 🐛 fix typo ([`381f89f`](https://github.com/datajoint/element-deeplabcut/commit/381f89fff2f5e2ff5a79fbdc9959f083f267a6a8))

* fix(CICD): 🐛 fix typo ([`e0af5ca`](https://github.com/datajoint/element-deeplabcut/commit/e0af5caff326bd2062bea9cd6685f9acfc77fc25))

* fix(CICD): 🐛 update changelog to unrelease ([`80c2f59`](https://github.com/datajoint/element-deeplabcut/commit/80c2f590a06ba9ad9b7d373b2c223bc590d3cd6f))

* fix(CICD): 🐛 rollback changelog ([`ccde295`](https://github.com/datajoint/element-deeplabcut/commit/ccde2958133405ae8df8112f943445275fb10665))

* fix(CICD): 🐛 fix DISTRO to DIST ([`ef00305`](https://github.com/datajoint/element-deeplabcut/commit/ef00305950938481e1d9c07484936dbee76c50f5))

* fix(CICD): 🐛 add Dockerfile ([`02d3a95`](https://github.com/datajoint/element-deeplabcut/commit/02d3a953fcfe9938827546dd07a66972a735a518))

* fix(CICD): 🐛 add docker-compose-build.yaml ([`a77db0c`](https://github.com/datajoint/element-deeplabcut/commit/a77db0c988ca9c74b7f25ad7007d1f9e7355d75f))

* fix(CICD): 🐛 fix push trigger ([`9bd44fb`](https://github.com/datajoint/element-deeplabcut/commit/9bd44fb8b0b9f9b8968af4cc4281e4858e839dbd))

* fix(CICD): 🐛 refer dev fork CI ([`5610b32`](https://github.com/datajoint/element-deeplabcut/commit/5610b32c62c3ffcacaa5944c330962ad020425fe))

### Test

* test(CICD): 🔖 ([`1055555`](https://github.com/datajoint/element-deeplabcut/commit/1055555ab1739d2ede1464cad7a4a3d2462c35ff))

* test(CICD): 🐛 job name ([`70918a7`](https://github.com/datajoint/element-deeplabcut/commit/70918a7160e52c274cc17f755d3999c552d814e6))

### Unknown

* Merge pull request #35 from yambottle/main

changelog fix type | add test release cicd ([`66802d6`](https://github.com/datajoint/element-deeplabcut/commit/66802d675d5193596b434ca577b8f212b6c0dd9a))

* resolve conflict ([`31bfde5`](https://github.com/datajoint/element-deeplabcut/commit/31bfde545c8994e30456f1d0430bd83dea4598d1))

* Merge pull request #37 from kabilar/main

Remove direct dependency for PyPI release ([`6ee17ef`](https://github.com/datajoint/element-deeplabcut/commit/6ee17efd3a3140173648bd780f05d437a179bf81))

* Update changelog ([`0ded37e`](https://github.com/datajoint/element-deeplabcut/commit/0ded37eab4226fe9488b1c3ad7dc0a6cbcc2fe59))

* Remove dependency for PyPI release ([`6ced597`](https://github.com/datajoint/element-deeplabcut/commit/6ced59744a6dd4f4274dc78cb8e5f5973e86c413))

* Merge pull request #33 from yambottle/main

Enable reusable CICD ([`b5fc591`](https://github.com/datajoint/element-deeplabcut/commit/b5fc59190e4670b8381fc4c48a8ade2857c3d119))

* revert ([`a85e6ac`](https://github.com/datajoint/element-deeplabcut/commit/a85e6ac1c49bfcd4089960712a9d081e2ee5b82b))

* revert ([`fe34dcf`](https://github.com/datajoint/element-deeplabcut/commit/fe34dcfa36865ffde5e6e1c11ff84c0143e4bd69))

* revert videotype ([`21abbf5`](https://github.com/datajoint/element-deeplabcut/commit/21abbf529eb92686447afa14cdc7ea967827d16e))

* misc ([`69e58f4`](https://github.com/datajoint/element-deeplabcut/commit/69e58f43064499e591576a29b1c81078a4493719))

* freeze dlc version ([`dc81963`](https://github.com/datajoint/element-deeplabcut/commit/dc819634ec49b431a45deb88f630b258346123bf))

* Merge pull request #32 from tdincer/main

modify do_pose_estimation to write config.yaml in dlc_project_path ([`9bcb177`](https://github.com/datajoint/element-deeplabcut/commit/9bcb1779d3feb68b3170c9ad2fca86e4579834e2))

* modify do_pose_estimation to write config.yaml in dlc_project_path ([`9b5aeef`](https://github.com/datajoint/element-deeplabcut/commit/9b5aeef7c2990842c9fead86b9098956b382de43))

* Merge pull request #31 from tdincer/main

revert path find ([`7cc275a`](https://github.com/datajoint/element-deeplabcut/commit/7cc275ab29c1a750abe82120bb74a112e62a0828))

* add optional project name ([`682f67a`](https://github.com/datajoint/element-deeplabcut/commit/682f67aa74700af41284f6515f784a702a8ac644))

* Equipment -&gt; Device ([`664cec2`](https://github.com/datajoint/element-deeplabcut/commit/664cec233e1812ea24a5af593e979cd2d81d2446))

* revert path find ([`5a22175`](https://github.com/datajoint/element-deeplabcut/commit/5a221755f357771dba8b0f40e546cfef783b7fb4))

* Merge pull request #29 from tdincer/main

add yaml and cv2 imports ([`d5b1858`](https://github.com/datajoint/element-deeplabcut/commit/d5b185804c744272824d8e22c6d2a6fba8dace91))

* change changelog ([`9a97928`](https://github.com/datajoint/element-deeplabcut/commit/9a97928cf5e45f8ab609fbbaeba3d9a80bc8e075))

* fix project path ([`c816daf`](https://github.com/datajoint/element-deeplabcut/commit/c816daffc37c466c3ade4b7c50dc5d7c5d494585))

* revise model docstring ([`6fbc063`](https://github.com/datajoint/element-deeplabcut/commit/6fbc063fe3f1049f71a5243d8fcb9a186f5cc225))

* adopt function name to dlc version ([`db05b90`](https://github.com/datajoint/element-deeplabcut/commit/db05b90697d4b8c6cf787b6e18ed931e7d885c00))

* Merge branch &#39;main&#39; of https://github.com/tdincer/element-deeplabcut ([`3753ac0`](https://github.com/datajoint/element-deeplabcut/commit/3753ac0696bd596e08db19267869d2c52a3f8402))

* Merge branch &#39;datajoint:main&#39; into main ([`4f30c5d`](https://github.com/datajoint/element-deeplabcut/commit/4f30c5dd17ee5387c3e5ff8dcb802c2e3f21a846))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut ([`2ff1779`](https://github.com/datajoint/element-deeplabcut/commit/2ff1779db9ab50706e068723e6d8bd4605cf66a7))

* Merge pull request #28 from tdincer/main

move to &#39;Device&#39; upstream table. ([`8b4d910`](https://github.com/datajoint/element-deeplabcut/commit/8b4d910f3cfacb6a9ffdb10f88e1ec548c84ba5a))

* add changelog ([`1e4b489`](https://github.com/datajoint/element-deeplabcut/commit/1e4b4898d1620e36ce019ea10acc14fe1669ab41))

* add import yaml - forgotten from the last time ([`cced805`](https://github.com/datajoint/element-deeplabcut/commit/cced805e55ea367703fd9870b2ee480a6a19aedb))

* fix docstring of get_trajectory ([`7362d2c`](https://github.com/datajoint/element-deeplabcut/commit/7362d2c58897c5f025b6ae373e01c76213a825f1))

* add development.yaml ([`76ea933`](https://github.com/datajoint/element-deeplabcut/commit/76ea93367fbaef0399ff9c67e7151e5a0b0de26a))

* Merge branch &#39;main&#39; of https://github.com/tdincer/element-deeplabcut ([`60ef71f`](https://github.com/datajoint/element-deeplabcut/commit/60ef71ffd3e27af21c09ff85c92d0bf6c6442608))

* Update element_deeplabcut/model.py

Co-authored-by: Dimitri Yatsenko &lt;dimitri@datajoint.com&gt; ([`be07c8b`](https://github.com/datajoint/element-deeplabcut/commit/be07c8beedebb8d4a82e5229751bba2dfe697c2c))

* move imports back to the make functions ([`02a4f64`](https://github.com/datajoint/element-deeplabcut/commit/02a4f64dc6183eab44600ef36852720b52e37a19))

* Equipment -&gt; Device ([`bbf2dcc`](https://github.com/datajoint/element-deeplabcut/commit/bbf2dcca0a567c531c6dff59b82ecbe2cd633dff))

* remove version check from scorer_legacy ([`c3fe727`](https://github.com/datajoint/element-deeplabcut/commit/c3fe7270efa95b1c4de70011977bd29fede9cfff))

* put back the reference ([`1ed1043`](https://github.com/datajoint/element-deeplabcut/commit/1ed1043de125f89c13e97d0fa6b51376094071f3))

* bug fix ([`d2d7bd5`](https://github.com/datajoint/element-deeplabcut/commit/d2d7bd5e36f2fb9a251c0ea79fd24ba62b6d06fb))

* fix terminology ([`2040e37`](https://github.com/datajoint/element-deeplabcut/commit/2040e37e82a3c632383e37887318a3fc5211d982))

* improved training data handling ([`b7dc27b`](https://github.com/datajoint/element-deeplabcut/commit/b7dc27b81ad691f4dc1367c12e8f88d8e429fd16))

* Merge pull request #23 from CBroz1/dj

blackify ([`699a217`](https://github.com/datajoint/element-deeplabcut/commit/699a2178dcbc9a502ecfe2345e898db2594e25a5))

* Bump version in changelog ([`993377e`](https://github.com/datajoint/element-deeplabcut/commit/993377e8033cec09c3b8c0a511c0fb6c408107f1))

* Bump version in changelog ([`a4ccd34`](https://github.com/datajoint/element-deeplabcut/commit/a4ccd347159ce237172fae1c6ee1dd4582a66ea5))

## v0.1.0 (2022-05-10)

### Unknown

* Bump version ([`ca2738f`](https://github.com/datajoint/element-deeplabcut/commit/ca2738f3a80213c8ef33b30aceae7f8b08df247f))

* blackify ([`8db4a54`](https://github.com/datajoint/element-deeplabcut/commit/8db4a541184379e11bc156f18fcc1b744f03cea4))

* Merge pull request #22 from CBroz1/main

Device -&gt; Equipment ([`b88c8dd`](https://github.com/datajoint/element-deeplabcut/commit/b88c8dd6051445928d5eb2916201b4b60ea33a0a))

* Device -&gt; Equipment ([`c6519c9`](https://github.com/datajoint/element-deeplabcut/commit/c6519c905d12f4c4805efb6fa400254306ad16c7))

* Merge pull request #19 from CBroz1/main

Update diagrams and YT link in README ([`5a9595d`](https://github.com/datajoint/element-deeplabcut/commit/5a9595d0c61916c50a797c0e08de5293744cab4e))

* add element_interface Issue #21 ([`7f2eddd`](https://github.com/datajoint/element-deeplabcut/commit/7f2eddde74c52613db855f7ce7a853267c2bd407))

* Diagrams: +subject. Link: YouTube thumbnail ([`f3bbd7f`](https://github.com/datajoint/element-deeplabcut/commit/f3bbd7ff3b050a24e338075923d6de772472181b))

* Update diagrams and YT link in README ([`141230d`](https://github.com/datajoint/element-deeplabcut/commit/141230dd6fcd1d135a98fdf7a248d29d59588437))

* Merge pull request #18 from ttngu207/main

minor update in `File`  table for consistency ([`0c71ecb`](https://github.com/datajoint/element-deeplabcut/commit/0c71ecbd60730a322b6631de1667155fde1f3bbe))

* Update element_deeplabcut/model.py

Co-authored-by: Chris Brozdowski &lt;CBrozdowski@yahoo.com&gt; ([`55e3040`](https://github.com/datajoint/element-deeplabcut/commit/55e30405ddf59efbb9ae69439363989234e54f20))

* non-nullable recording duration ([`4eb8a26`](https://github.com/datajoint/element-deeplabcut/commit/4eb8a260974603e10d0f62ffc6c9dbb99e7a7a17))

* minor update in `File`  table for consistency ([`1e6a8f0`](https://github.com/datajoint/element-deeplabcut/commit/1e6a8f0949854c3ebae53be6d17ff5db6d33ae11))

* Merge pull request #16 from kabilar/main

Update README ([`1062b4b`](https://github.com/datajoint/element-deeplabcut/commit/1062b4b26f75c310cb574cd5f13550ae11572b6a))

* Update README.md

Co-authored-by: Chris Brozdowski &lt;CBrozdowski@yahoo.com&gt; ([`e5dde7a`](https://github.com/datajoint/element-deeplabcut/commit/e5dde7a1416c817535279b3bd1b41d7f7f6bec4c))

* Update README.md

Co-authored-by: Chris Brozdowski &lt;CBrozdowski@yahoo.com&gt; ([`1f53b68`](https://github.com/datajoint/element-deeplabcut/commit/1f53b68fc637e8e11b559abe5d9766050bd01465))

* Update format ([`f631195`](https://github.com/datajoint/element-deeplabcut/commit/f6311955d6b38b93f701c014ab01193670c5e60e))

* Fix format ([`9f39af4`](https://github.com/datajoint/element-deeplabcut/commit/9f39af4d5e1aefbf04dfa537755d9a38748799a2))

* Fix typo ([`c7300eb`](https://github.com/datajoint/element-deeplabcut/commit/c7300eb009a7a802edab7c7032e02b1cea18c45b))

* Add links to elements.datajoint.org ([`e46c666`](https://github.com/datajoint/element-deeplabcut/commit/e46c6668b1f8d0b3591f94be3736846532c38b24))

* Add citation section ([`edf2aef`](https://github.com/datajoint/element-deeplabcut/commit/edf2aefcfeea47062eff8bb6033dd3fe893e0bc5))

* Merge pull request #15 from ttngu207/main

add RecordingInfo ([`705f154`](https://github.com/datajoint/element-deeplabcut/commit/705f1548b9dd0a03d1e3ff2eaa77b6c6c4d8368d))

* Update element_deeplabcut/model.py

Co-authored-by: Chris Brozdowski &lt;CBrozdowski@yahoo.com&gt; ([`c4ee40a`](https://github.com/datajoint/element-deeplabcut/commit/c4ee40ab38459c8a847b18c6dd30bb89e0c66863))

* add RecordingInfo ([`537c2ce`](https://github.com/datajoint/element-deeplabcut/commit/537c2cecc951ac6bfab5d1282be8a507dedbf806))

* Merge pull request #8 from CBroz1/main

`model.Model.BodyPart` insertion fix; README updates ([`6086009`](https://github.com/datajoint/element-deeplabcut/commit/6086009d157862e28214c6dacf3f3e85f35ac677))

* Apply suggestion from code review

Co-authored-by: Thinh Nguyen &lt;thinh@vathes.com&gt; ([`9f67d08`](https://github.com/datajoint/element-deeplabcut/commit/9f67d087f8c04406de88a1eae3ea71bed4ae00a1))

* fix model.Model.BodyPart table insertion; remove numpy require ([`2879ae1`](https://github.com/datajoint/element-deeplabcut/commit/2879ae1b946f4c24166a0a418a8cb4aab5fccebe))

* Merge branch &#39;main&#39; of https://github.com/datajoint/element-deeplabcut ([`65a4e60`](https://github.com/datajoint/element-deeplabcut/commit/65a4e60e33d72d44444b041ce8f9d91007bf53aa))

* Merge pull request #13 from datajoint/requirement-patch

Missing 0 on numpy requirement ([`e8961ff`](https://github.com/datajoint/element-deeplabcut/commit/e8961fffe0457ef43c93f5fb2735e1416bb05de4))

* Missing 0 on numpy requirement ([`df3c337`](https://github.com/datajoint/element-deeplabcut/commit/df3c33735b0af6ba593dbc2d8c96f6e3959f9295))

* Merge pull request #12 from kabilar/main

Minor text fix ([`9199a80`](https://github.com/datajoint/element-deeplabcut/commit/9199a8058865d8c6e1e1e6fd33f7230205add871))

* Minor text fix ([`a2bd409`](https://github.com/datajoint/element-deeplabcut/commit/a2bd4093ca29678d99157259cc08ff35f2d7f5d3))

* Merge pull request #5 from CBroz1/main

Pushing from `cbroz1:dev` discussion to `datajoint:main` ([`b8b5137`](https://github.com/datajoint/element-deeplabcut/commit/b8b5137673a6cd92794a0080098819c28f6efa1a))

* minor README updates ([`32524e2`](https://github.com/datajoint/element-deeplabcut/commit/32524e2bf9085bfdaf101f8039d0cb2a10e8191c))

* Merge pull request #5 from CBroz1/dev

Update schema split: `train`, `model` ([`b067e9f`](https://github.com/datajoint/element-deeplabcut/commit/b067e9fd5213139859e4781f54f8d80581cd731f))

* remove version info from __init__.py ([`9104105`](https://github.com/datajoint/element-deeplabcut/commit/910410511b22161683f38d50f537b8eac8068aa8))

* Apply suggestions from code review

Co-authored-by: Thinh Nguyen &lt;thinh@vathes.com&gt; ([`db6ecfb`](https://github.com/datajoint/element-deeplabcut/commit/db6ecfbbf329fd070ae40816927d03955d6a089d))

* See Details. Update functions for separate video tables across schemas

helper funcs: fixed bug where root_dir[0] would get appended to root_dirs whenever
              get_processed_dir was called.
extract_new_bodyparts: added verbose arg to prevent duplicate print when calling
                       model.Model.insert_new_model
insert_new_model: because `BodyPart.extract_new_body_parts` returns a list, checking the
                  truth value is ambiguous. Changed to &#39;is not None&#39;
infer_ouput_dir: remove _linking_module for VideoRecording table
insert_new_params: Enforce int type on paramset_idx input. Previously failed to return
                   when attempting to insert a duplicate bc str(x)!=int(x) ([`26e6b44`](https://github.com/datajoint/element-deeplabcut/commit/26e6b4421247d506937f257dd8aba29684148cc8))

* update diagrams ([`6d74ab7`](https://github.com/datajoint/element-deeplabcut/commit/6d74ab7b918bbb00e975d758163d4f6beab8761f))

* VideoRecording to model schema ([`b842547`](https://github.com/datajoint/element-deeplabcut/commit/b84254785e42d2ae07e344bbf11bb84e2979ee51))

* typo fix ([`3371785`](https://github.com/datajoint/element-deeplabcut/commit/337178565023b81c533756417c93f8c4dc8308a8))

* update documentation ([`c7a3b03`](https://github.com/datajoint/element-deeplabcut/commit/c7a3b03297c977e1a0cafd3d93173314ba51f7fb))

* 3 -&gt; 2 schema ([`989b272`](https://github.com/datajoint/element-deeplabcut/commit/989b272c8fb1a39155eec6334cf5313318e610a0))

* Split dlc schema ([`09b4c7d`](https://github.com/datajoint/element-deeplabcut/commit/09b4c7d11c0091ec6c4dbbe0cdc2adb120b3510a))

* minor readme edit ([`bc054fb`](https://github.com/datajoint/element-deeplabcut/commit/bc054fb4336f1b165d77018119fc7a9d979f6bd3))

* Merge pull request #2 from CBroz1/dev

MVP here we come ([`015843a`](https://github.com/datajoint/element-deeplabcut/commit/015843a86af5aa17a7253e875bdfb23b5dfcfb02))

* Merge branch &#39;main&#39; into dev ([`b9fd1c9`](https://github.com/datajoint/element-deeplabcut/commit/b9fd1c9ac9c9404196a53f371d49f6ed5583c1da))

* rename `LabeledFrame` -&gt; `File` - to be more genelizable ([`8e4d7ce`](https://github.com/datajoint/element-deeplabcut/commit/8e4d7cedd58110cd5477c3b98267bffcbd8131ae))

* draft - using `TrainingVideo` table for training instead of `VideoRecording` ([`0e8cb2a`](https://github.com/datajoint/element-deeplabcut/commit/0e8cb2a10c9224d0c514f853bb14d5ba7ab109fe))

* edit README ([`2585ef3`](https://github.com/datajoint/element-deeplabcut/commit/2585ef3528fa7f2a03af42e850fd3c6053b2fbaa))

* Rebasing

PEP8
README: add note on dependency conflict numpy==1.2
/images/: update diagram
dlc schema:
- remove arg for get_dlc_processed_dir
- Add note on scorer_legacy
- add docstrings
- add note on continue from prev snapshot
- add set shuffle/trainindex/maxiters to int for model training make
- add `TrainingVideo` table for training instead of `VideoRecording`
    - `LabeledFrame` -&gt; `File` generalizable part table
- BodyPart.insert_new
    - refactor logic for yaml type check
    - separate BodyPart functions - return list then insert
- Model.insert_new_model - refactor config yaml type check
    - Add scorer legacy check
    - add dlc version insertion
- ModelEvaluation - make items nullable bc saw eval that didn&#39;t return some value
    - refactor config yaml type check
- PoseEstimationTask - permit estimation paramset to pass to analyze_videos
    - Type set to string for concatenating output dir
    - add insert helper function
- PoseEstimation - permit output_dir as fullpath, per &#39;relative&#39; arg in task table
    - permit passing analyze_videos params
    - permit null analyze_video_param
dlc_reader:
- prev had separate output dir and project dir... removing
- do_pose_estimation - permit args passed from PoseEstimationTask.params
- adjust yml_path in reader to remove dlc_dir.parent
Apply suggestions from code review ([`3c8ff44`](https://github.com/datajoint/element-deeplabcut/commit/3c8ff44ce1ac6912000b6a08b3eee8fff59b9ba3))

* separate BodyPart functions - return list then insert ([`fb72d8c`](https://github.com/datajoint/element-deeplabcut/commit/fb72d8c2fdc5d66d48519712d22530c0d9e30ec1))

* null analyze_video_param handling ([`fbf3b7e`](https://github.com/datajoint/element-deeplabcut/commit/fbf3b7ec2e38eed9813d4ba30005ef39ac7236c2))

* additional code review suggestions ([`84f0d84`](https://github.com/datajoint/element-deeplabcut/commit/84f0d8485905a0cdd3cf35b8a7e9b6416026f7b9))

* Apply suggestion from code review

Co-authored-by: Thinh Nguyen &lt;thinh@vathes.com&gt; ([`540ba06`](https://github.com/datajoint/element-deeplabcut/commit/540ba06ae6fcdd7111c9db04ad394a9fe7327b1b))

* update diagram ([`88eb82f`](https://github.com/datajoint/element-deeplabcut/commit/88eb82f5272d9440e9e8503de6d2159158f5870f))

* See details - long list

README: add note on dependency conflict numpy==1.2

dlc schema:
- remove arg for get_dlc_processed_dir
- Add note on scorer_legacy
- add docstrings
- add note on continue from prev snapshot
- add set shuffle/trainindex/maxiters to int for model training make
- BodyPart.insert_new - refactor logic for yaml type check
- Model.insert_new_model - refactor config yaml type check
    - Add scorer legacy check
    - add dlc version insertion
    - add body part description arg
- ModelEvaluation - make items nullable bc saw eval that didn&#39;t return some value
    - refactor config yaml type check
- PoseEstimationTask - permit estimation paramset to pass to analyze_videos
    - Type set to string for concatenating output dir
    - add insert helper function
- PoseEstimation - permit output_dir as fullpath, per &#39;relative&#39; arg in task table
    - permit passing analyze_videos params

dlc_reader:
- add conditional logic for if passed the output dir instead of project dir
- assumes output dir is under project dir
- do_pose_estimation - permit args passed from PoseEstimationTask.params ([`cef65ed`](https://github.com/datajoint/element-deeplabcut/commit/cef65ed8d4dc27ee672f887baa704c49cb5e048f))

* PEP8 ([`aa4961e`](https://github.com/datajoint/element-deeplabcut/commit/aa4961ea2a7fcc6a375edddaee22562f981a8fef))

* Merge pull request #4 from ttngu207/main

prototype revision no 2 ([`1d990db`](https://github.com/datajoint/element-deeplabcut/commit/1d990db72fcbfa8fd66a108b9c65539d6d036fd0))

* bugfix import errors ([`bdf7fb1`](https://github.com/datajoint/element-deeplabcut/commit/bdf7fb128070d65b445f00bb5695c6b1a58481e3))

* bugfix ([`23ff3d9`](https://github.com/datajoint/element-deeplabcut/commit/23ff3d97ba83eedb050d338f33ca618ba5090011))

* bugfix ([`7cd8f25`](https://github.com/datajoint/element-deeplabcut/commit/7cd8f251f27153ebe3ae50ce0c658cb8a7ebff9e))

* bugfix ([`18b3177`](https://github.com/datajoint/element-deeplabcut/commit/18b31772fc90feecb7b0ab3a32958bc8f6239b05))

* address review comment ([`b8df6d7`](https://github.com/datajoint/element-deeplabcut/commit/b8df6d7a676702d26f8110682b8813e915bef118))

* remove the need for `get_session_directory` - add helper method to infer output dir ([`06daffc`](https://github.com/datajoint/element-deeplabcut/commit/06daffc7a96072e5f426120ff40536f9e1212901))

* video_paths for model training ([`ed63cc4`](https://github.com/datajoint/element-deeplabcut/commit/ed63cc458e20fa37fae1e2574229b996bbca538f))

* accounts for `model_prefix` ([`3ad6838`](https://github.com/datajoint/element-deeplabcut/commit/3ad6838455f41fe669a0cbfda93b25385babd97a))

* update `ModelTraining` &#39;s `make()` - code cleanup ([`833bb7e`](https://github.com/datajoint/element-deeplabcut/commit/833bb7ecbb5ac7c37b4f0af0e6be7c25bca969fe))

* Merge branch &#39;dev&#39; of https://github.com/CBroz1/element-deeplabcut ([`62e2407`](https://github.com/datajoint/element-deeplabcut/commit/62e2407b30b9a36edf35b2fc333a58341e2166e8))

* Update dlc_draft.py ([`d4acd5f`](https://github.com/datajoint/element-deeplabcut/commit/d4acd5f6fa1d81e4686007656a7e1a157dcdb336))

* rename, restructure ([`511980e`](https://github.com/datajoint/element-deeplabcut/commit/511980e31e9c39c4535b53c3d2b8048090aa7283))

* add make for pose estimation ([`3140065`](https://github.com/datajoint/element-deeplabcut/commit/3140065cad69ca18524e57e9461a5212f7cdbf86))

* add dlc loader ([`a9a2e38`](https://github.com/datajoint/element-deeplabcut/commit/a9a2e3883c32cdfc1787ab8b41811fd88969ed3b))

* revised draft dlc ([`8ee7888`](https://github.com/datajoint/element-deeplabcut/commit/8ee788899772dcc0a4d52f79cdf0dd683add41c8))

* Merge pull request #3 from CBroz1/dev

Add functions to link tables ([`b498a02`](https://github.com/datajoint/element-deeplabcut/commit/b498a0295a4c9eb39d8c009f32a44dd8a11ebcc4))

* Update element_deeplabcut/dlc.py

Co-authored-by: Thinh Nguyen &lt;thinh@vathes.com&gt; ([`046064d`](https://github.com/datajoint/element-deeplabcut/commit/046064d1dbe7942e91f910ec993c6b106dbac31b))

* update diagram, readme ([`f264c6d`](https://github.com/datajoint/element-deeplabcut/commit/f264c6d60752f6061a9ddffa8eda6eda9a072c87))

* debug trajectory func ([`aa22fe6`](https://github.com/datajoint/element-deeplabcut/commit/aa22fe639503efddf6ed427cad66e846927d6fda))

* Rebase. See Details

rename, restructure
Update dlc_draft.py
Ingest function drafts ([`adf3e3f`](https://github.com/datajoint/element-deeplabcut/commit/adf3e3f9aec0b1d1346d350a6971cd717b3a629a))

* add make for pose estimation ([`294a3e8`](https://github.com/datajoint/element-deeplabcut/commit/294a3e8bd07b6f3de4482b8af4e4ca6d421e24b1))

* add dlc loader ([`3c8ace2`](https://github.com/datajoint/element-deeplabcut/commit/3c8ace2ff7bdb38d6401a0e1c7e55e3c4e77e24e))

* revised draft dlc ([`340bdee`](https://github.com/datajoint/element-deeplabcut/commit/340bdeee2b47b3e804f014703c2cca91aae097f0))

* Merge pull request #2 from ttngu207/main

Proposed schema design ([`1dd0f1e`](https://github.com/datajoint/element-deeplabcut/commit/1dd0f1ef2fca909b68c6b18a7cfb6e5bd88a6911))

* dlc_draft ([`f44efef`](https://github.com/datajoint/element-deeplabcut/commit/f44efef7e18b24e0901278282dc675492442302e))

* Merge pull request #1 from CBroz1/dev

Dev ([`6f2b9e0`](https://github.com/datajoint/element-deeplabcut/commit/6f2b9e0f1e916a802b3cf1da680c8289a95e0bdc))

* minor table structure edits with Thinh ([`6029422`](https://github.com/datajoint/element-deeplabcut/commit/6029422ab948fd80b4517101b08cc1e148a81f17))

* Merge from CBroz1/dev

Recent work ([`738999d`](https://github.com/datajoint/element-deeplabcut/commit/738999d482e205c1fd3a58c5c610a1769fadef6e))

* add diagram, README+CHANGELOG clarity ([`7ebdfc3`](https://github.com/datajoint/element-deeplabcut/commit/7ebdfc372ed97b144aad1935a8c98701b845a03d))

* NotImplementedError for multi-animal ([`1668f8f`](https://github.com/datajoint/element-deeplabcut/commit/1668f8fb630f35d61a7a31140a1e7488cd5d57c3))

* Cleanup: rm README notes and incomplete files ([`07977ab`](https://github.com/datajoint/element-deeplabcut/commit/07977abf8b9b0c682ad597c0577fb2769593f84d))

* Revise ingestion. Add 2d return trajectory. See details

dlc.py:
- limit imports of DLC proper to only needed funcs
- separate schema activation
- config parameters to separate table following element-array-ephys
- load fps from model files
- remove user choice points
- use DLC functions to load and pick between multiple files

changelog/version.py: revise version number
.github/ISSUES: add bug_report and feature request ([`44dbe9c`](https://github.com/datajoint/element-deeplabcut/commit/44dbe9c1accd5e4e1fae6e751cd23ecc9cae5194))

* Functional 2D single-animal ingestion ([`873414f`](https://github.com/datajoint/element-deeplabcut/commit/873414f852fedb0eeb0879cedd217fb382db2a62))

* Load standard model. Recording-&gt;Model-&gt;Estimates ([`c516ea0`](https://github.com/datajoint/element-deeplabcut/commit/c516ea0aded44531a2721178415d1628b76d9834))

* README updates; tables WIP ([`f9f9b9a`](https://github.com/datajoint/element-deeplabcut/commit/f9f9b9a3502fcc01763c985e21bf8798c7b8fc37))

* revert ([`9b0af64`](https://github.com/datajoint/element-deeplabcut/commit/9b0af64453b5f2c2cb1a948d76e30cd47ec5626a))

* minor readme update ([`3165a6f`](https://github.com/datajoint/element-deeplabcut/commit/3165a6f0ab03f69f9d0dfb5f71046a082561e985))

* minor syntax fixes ([`626fa2d`](https://github.com/datajoint/element-deeplabcut/commit/626fa2da8549d3769cf9296b39a3071a3aebf72b))

* add .DS_Store ([`2f91758`](https://github.com/datajoint/element-deeplabcut/commit/2f91758469e16f798d8290749fea585d683951d4))

* major file structure, drafting ([`c43171a`](https://github.com/datajoint/element-deeplabcut/commit/c43171a688aa0f811a6f727d2b8b28b8b7d77687))

* Add files via upload ([`5d4e70d`](https://github.com/datajoint/element-deeplabcut/commit/5d4e70d4a9e49ea3ee32cf94d5dcf7359b2330b3))

* Initial commit rebased ([`31e4581`](https://github.com/datajoint/element-deeplabcut/commit/31e458180bc5205644f6e8c26c13ca93ae516dff))

* Initial commit ([`d8ffc2a`](https://github.com/datajoint/element-deeplabcut/commit/d8ffc2aa16858f7666f887910764890e02312914))

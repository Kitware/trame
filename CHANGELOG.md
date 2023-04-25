# Changelog

<!--next-version-placeholder-->

## v2.4.0 (2023-04-25)
### Feature
* **py-client:** Enable cross trame-server communication ([`afab046`](https://github.com/Kitware/trame/commit/afab0462c8fedc9b8b0f70f86d7eb08f3ead9fe3))

### Documentation
* **api:** List external widgets ([`a333db1`](https://github.com/Kitware/trame/commit/a333db1dfccd9f3a838d25cdded59acfe9cc4c44))
* **docker:** Fix docker remote rendering example ([`ab55187`](https://github.com/Kitware/trame/commit/ab5518795a3c8b5827f05e2e650e39bff32e55ac))
* **osmesa:** Update requirements.txt for remote rendering ([`7b0fcbd`](https://github.com/Kitware/trame/commit/7b0fcbdf564b936ad1b7f5d927d4e0fe2fe1824a))
* **docker:** VTK remote rendering ([`e11ff23`](https://github.com/Kitware/trame/commit/e11ff23beadb26ad16aa56f2925a0b92a62c056c))
* **examples:** Add docker remote rendering example ([`7a847a0`](https://github.com/Kitware/trame/commit/7a847a0ca1294cbff2f191275a09fe7007d6f66e))
* **vue3:** New template handling syntax ([`fbaffe3`](https://github.com/Kitware/trame/commit/fbaffe301a6a0d747d80782c9e7e29a529e20763))
* **vtk:** Update example with latest trame-vtk ([`f306d2d`](https://github.com/Kitware/trame/commit/f306d2d37eb668362773e6b5e3d3ce0f012a9630))
* **vue23:** Clarify some aspect ([`a5e2a5a`](https://github.com/Kitware/trame/commit/a5e2a5ac2223174f1ba128fbdd486b94f750f8f2))
* **website:** Update to add doc on vue2/3 ([`d70f097`](https://github.com/Kitware/trame/commit/d70f097c173cfd572ebeae51b8ddb90a939d9d6a))

## v2.3.2 (2023-02-14)
### Fix
* **www:** Allow www tool to support either vue2 or vue3 ([`363dd53`](https://github.com/Kitware/trame/commit/363dd5336034dbd9d5c5d03ce13ea242aa5f99c0))

## v2.3.1 (2023-02-10)
### Fix
* **testing:** Add testing helpers ([`493803d`](https://github.com/Kitware/trame/commit/493803d26b8c8d33b1f28c59cd5cdabb6c713636))

### Documentation
* **table:** Handle dynamic table ([`be314bf`](https://github.com/Kitware/trame/commit/be314bf58eef73dd0394f1dcc1c7735720fdcf73))

## v2.3.0 (2023-02-08)
### Feature
* **client_type:** Preparation for 3.x release ([`b88a994`](https://github.com/Kitware/trame/commit/b88a994e2acea87bf624340a178022158f00a79b))

### Documentation
* **website:** Update value proposition ([`e96749c`](https://github.com/Kitware/trame/commit/e96749c2360294ab5527d75052e2804dcc1aa210))
* **utils.tree:** Add API doc ([`2818473`](https://github.com/Kitware/trame/commit/28184737d7712f9ffe749ac3543bf3b43f4200fd))
* **hot_reload:** Deprecate @reloading example ([`96b4eb5`](https://github.com/Kitware/trame/commit/96b4eb5e5bd036ebc2816870022dcbbefdbc04ac))
* **hot_reload:** Make content center ([`e6aec3f`](https://github.com/Kitware/trame/commit/e6aec3fb41a6edecb379d2d7651ca3ecb40fe45f))

## v2.2.6 (2023-01-20)
### Fix
* **hot_reload:** Remove old code ([`7fc2948`](https://github.com/Kitware/trame/commit/7fc2948a61a2b304f72648cae062be2a1f52b697))

### Documentation
* **hot_reload:** Add example ([`f0f3cc8`](https://github.com/Kitware/trame/commit/f0f3cc8238677a7b2b2afd4585881873132dd97d))
* **issues:** Add issue code base ([`f177d4e`](https://github.com/Kitware/trame/commit/f177d4e35e855542513e17895092882bcc2d8521))
* **reloading:** Allow dynamic method reloading ([`06be552`](https://github.com/Kitware/trame/commit/06be55252f885ddf7ac917b47f6a5149b3cdb756))
* **Example:** Add cursor example ([`78e31cc`](https://github.com/Kitware/trame/commit/78e31cc1d9c593c58f664fbf10c9e943f9468e28))
* **DynamicLocalRemoteRendering:** Fix example to flush geometry ([`d0a1deb`](https://github.com/Kitware/trame/commit/d0a1deb65a5a8f6bbe7a2dcbbfda14a5ba563a91))
* **HPC:** Update hpc doc ([`208b711`](https://github.com/Kitware/trame/commit/208b71123da8428414d3c909b5d988cd665b9ac0))
* **website:** Update some website guides ([`7f58c1a`](https://github.com/Kitware/trame/commit/7f58c1a987066d92efbb460d65954695a912bd9e))
* **docker:** Update readme ([`ade4c25`](https://github.com/Kitware/trame/commit/ade4c25dc634d9dd30a25158e58c66d5a4b89322))

## v2.2.5 (2022-12-17)
### Fix
* **docker:** Separate out build and run steps ([`7393f1d`](https://github.com/Kitware/trame/commit/7393f1d44f9ddbc3d51db5cafbe88a4039ff9cc2))

### Documentation
* **docker:** Update readme ([`33e050d`](https://github.com/Kitware/trame/commit/33e050d986b22cadb377c57ac5d5d0ae714135a6))
* **docker:** Update docker to use build script ([`c3b7bd1`](https://github.com/Kitware/trame/commit/c3b7bd130af104549e2a18dafee4719ba59abf24))

## v2.2.4 (2022-12-12)
### Fix
* **docker:** Move apps.json creation into launcher section ([`eeb4a88`](https://github.com/Kitware/trame/commit/eeb4a886e39721b9059a7957ecdb3ea09d4a9b58))

## v2.2.3 (2022-12-11)
### Fix
* **docker:** Add build.sh script for easier builds ([`26effc0`](https://github.com/Kitware/trame/commit/26effc03b88cf5e86411fca80994c515ce29dee6))
* **docker:** Add ability to replace USE_HOST ([`3cd4dc3`](https://github.com/Kitware/trame/commit/3cd4dc321db1e404ec4ce8ae7db8747868b4d255))
* **docker:** Add additional build options ([`8ad6f44`](https://github.com/Kitware/trame/commit/8ad6f449347969e091bd178560edebb41c6aafb4))

### Documentation
* **selection:** Update pv selection with clear and click ([`0d06739`](https://github.com/Kitware/trame/commit/0d06739114ed3b37f838304b334295d6f93bf50d))
* **Style:** Add global css style example ([`00fa606`](https://github.com/Kitware/trame/commit/00fa60618aaff4f383b50e34e1c85d3a89d2e4b5))
* **Selection:** Add paraview remote rendering selection example ([`f9f6f7b`](https://github.com/Kitware/trame/commit/f9f6f7bbb23585e65bf2aaa0ccbfd00e342ebd14))
* **readme:** Handle typos ([`12879f2`](https://github.com/Kitware/trame/commit/12879f2e1f0e5f0f8550221278908a32180e2d5b))
* **examples:** Reformat using black ([`6fdc5a5`](https://github.com/Kitware/trame/commit/6fdc5a5f2bb52a2eff42ed4c1dfac9ec187cf372))
* **markdown:** Provide encoding at read time ([`2760bc2`](https://github.com/Kitware/trame/commit/2760bc28917fa31cc7f97ea8dd9a361cfe9f541c))

## v2.2.2 (2022-12-02)
### Fix
* **docker:** Add `wheel` to pip docker image ([`6f34a4e`](https://github.com/Kitware/trame/commit/6f34a4eead0e4f50372d3c6f524dfdd3f4a4b018))

### Documentation
* **examples:** Fix typo in vtkClass arg ([`4822ad3`](https://github.com/Kitware/trame/commit/4822ad3bbb60caab3630e8100cd71c3e4dc2d27e))
* **video:** Add video on landing page ([`76926cf`](https://github.com/Kitware/trame/commit/76926cfdcfabd724af34acd7e5bd613dd1e072c0))
* **video:** Add video on landing page ([`168a3c9`](https://github.com/Kitware/trame/commit/168a3c983bc71f5e03c27a0409d3f93f34683d54))
* **menu:** Update doc menu ([`89ee007`](https://github.com/Kitware/trame/commit/89ee0074f495a383ac171a2982db08f3c24abc88))
* **readme:** Remove the --pre in pip install command ([`dc01c70`](https://github.com/Kitware/trame/commit/dc01c70370c25fcb9e77fd86d46cd786a9a4e740))
* **deploy:** Add a deployment section ([`2b5e122`](https://github.com/Kitware/trame/commit/2b5e122e09658534f970c2f0b1bb9fc9043df0d9))
* **caprover:** Add info for caprover deploy ([`ea6fec4`](https://github.com/Kitware/trame/commit/ea6fec4b3c9d45241d00ff8b4913aab45200ebc0))
* **docker:** Add single file example ([`18fa307`](https://github.com/Kitware/trame/commit/18fa30792e6d6b8f8a8decc54d659ea306d36be9))
* **website:** Correct tutorial code examples ([`eb4a628`](https://github.com/Kitware/trame/commit/eb4a6283b2d1585d7c34b189c94871563817940e))
* **fileUpload:** Add validation example ([`9c81ea9`](https://github.com/Kitware/trame/commit/9c81ea995473f205348e5639d528ba9dde03521f))
* **example:** Switch view validation ([`662c5cb`](https://github.com/Kitware/trame/commit/662c5cb7c5092ff749edca94f15381cb72f22c6d))

## v2.2.1 (2022-10-21)
### Fix
* **rca:** Add trame-rca in default dependencies ([`7fa2253`](https://github.com/Kitware/trame/commit/7fa2253058aebe6e4e1c5150407f0019b275110b))

### Documentation
* **example:** Add stats to pv/wavelet example ([`c257a54`](https://github.com/Kitware/trame/commit/c257a54a0a06c2a5a0dc2f2879819a9f69effc24))
* **example:** Collaboration state async/busy update ([`792dd28`](https://github.com/Kitware/trame/commit/792dd28e288547f7dfe20eff5596c16554f80a70))
* **course:** Expanded and polished description of course ([`cc4e0ac`](https://github.com/Kitware/trame/commit/cc4e0ac9932ecdabefdcac5b67071bd461e937f8))
* **wavelet:** Add sc demo comparison ([`f9d5e36`](https://github.com/Kitware/trame/commit/f9d5e367eefcfa7c27e63e79daa1112b2dba3daf))
* **wavelet:** Add sc demo comparison ([`def850b`](https://github.com/Kitware/trame/commit/def850b5768e2099c0c5c3610117e02b0e8126c9))
* **course:** Update links of documents ([`73bb2e7`](https://github.com/Kitware/trame/commit/73bb2e71c68fb691aa8d265b410a5547accc656a))
* **course:** Add links to the course ([`4f79912`](https://github.com/Kitware/trame/commit/4f79912a039c10a46afadc85c084c31977b146e7))
* **vtk:** Rename trame.widgets.vtk to not confuse with vtk import ([`b480332`](https://github.com/Kitware/trame/commit/b48033261f364fd79f0dcd039b4c04c153eb67b1))
* **FiniteElementAnalysis:** Fix file chunk handling ([`7790cd1`](https://github.com/Kitware/trame/commit/7790cd1df397b6988fabf4238317a1957b57c3c7))
* **SurfacePicking:** Add jupyter helper function ([`76e6c8b`](https://github.com/Kitware/trame/commit/76e6c8b2a35e34e4a15ac6d3e479941b54500b36))
* **download:** Add binary download example ([`af70938`](https://github.com/Kitware/trame/commit/af70938509d966eae4cea5d76389ecdd9c97bc88))
* **examples:** Multi-server example ([`78008d9`](https://github.com/Kitware/trame/commit/78008d9a3b7ba0817df302ae1c81f93b7f618e5a))
* **paraview:** Add info for using conda ([`5e1160d`](https://github.com/Kitware/trame/commit/5e1160d72aef0d0b1edcab0450f90a03b9c0977c))
* **tutorial:** Fix typo in example ([`77b3a1b`](https://github.com/Kitware/trame/commit/77b3a1b6c262dfcfe50f10da26992ae023805f76))

## v2.2.0 (2022-08-29)
### Feature
* **ClientFile:** Add helper to handle multi-part upload file ([`d00907f`](https://github.com/Kitware/trame/commit/d00907f9b3806cb2d94b6565527956475848a7a2))

### Documentation
* **website:** Fix spacing ([`7073f5a`](https://github.com/Kitware/trame/commit/7073f5a401e0b9f626908784f3d8d73ac7316f9e))

## v2.1.2 (2022-08-24)
### Fix
* **simput:** Add simput as default dependency ([`b6ca24c`](https://github.com/Kitware/trame/commit/b6ca24ccace036122abe6dce27f5d51fab53fb2e))

### Documentation
* **examples:** Add validation examples ([`8a7e1ca`](https://github.com/Kitware/trame/commit/8a7e1ca1416e61014c31315096343c83e1c8f91e))
* **api:** Update client side API ([`738565f`](https://github.com/Kitware/trame/commit/738565fe1960aba916fd7bf6709de5b3f6a33c0a))
* **reverse-stop:** Test client to ask server to stop ([`1877a46`](https://github.com/Kitware/trame/commit/1877a46c9e2be8b4e0a6157de16851d362761734))
* **relay:** Add reverse connection and relay scenario ([`7cbfbf4`](https://github.com/Kitware/trame/commit/7cbfbf46bf1dc46850768909802da08d725c0944))
* **example:** Add validation for download with promise ([`51ad010`](https://github.com/Kitware/trame/commit/51ad0108a72f24a67449e05eba306581c0f818b9))
* **examples:** Ensure file browser appears in front ([`ef1a869`](https://github.com/Kitware/trame/commit/ef1a869dd4e6aa8c38a4da2dc3ebd1e1b47332f8))
* **examples:** Add tkinter file browser example ([`190b37d`](https://github.com/Kitware/trame/commit/190b37dbcf56c900db0e38031f953b5695685067))
* **coverage:** Remove codecov PR comment ([`49065a0`](https://github.com/Kitware/trame/commit/49065a0abb766c06c12972fa5022ee455d1fce9f))
* **website:** Improve language and grammar ([`6959dc8`](https://github.com/Kitware/trame/commit/6959dc8971f2bbe34c0afdfc90fe2fabde29c242))
* **coverage:** Add .coveragerc ([`41c4d62`](https://github.com/Kitware/trame/commit/41c4d62e7a6f5dba41fd9305b314c87fa8ed7b6f))
* **ci:** Add coverage and codecov upload ([`e6f3181`](https://github.com/Kitware/trame/commit/e6f3181c053c009017a95355721525dc502c5d35))
* **readme:** Add CI badge ([`c07b0d2`](https://github.com/Kitware/trame/commit/c07b0d22c673883e58914ea36489d49fc54b8ac4))
* **readme:** Fix invalid path for pict ([`97b4a3c`](https://github.com/Kitware/trame/commit/97b4a3cb0c5a2346775d4f921107772200c87670))

## v2.1.1 (2022-06-15)
### Fix
* **mimetypes:** Ensure javascript files get the correct mimetype ([`40a9618`](https://github.com/Kitware/trame/commit/40a9618af62da9f7d2b88bc333938c9ccc647487))

### Documentation
* **example:** Fix SimpleCone/RemoteRendering ([`498fd78`](https://github.com/Kitware/trame/commit/498fd7803505068cf269aa1ac83806e1b16d3d03))
* **contributing:** Add CONTRIBUTING.rst ([`9e51275`](https://github.com/Kitware/trame/commit/9e5127537c23b743b04cbafff3f5f21ba277344a))

## v2.1.0 (2022-06-04)
### Feature
* **ui:** Add virtual node ui manager with server ([`6956009`](https://github.com/Kitware/trame/commit/695600928f2bd3e3795c556d609eb11c93ba7c50))

### Documentation
* **welcome:** Update note ([`cee6461`](https://github.com/Kitware/trame/commit/cee64613717607cb374e9c2ca07f5d40f1c6c7c8))
* **intro:** Remove --pre from pip install command ([`f748dd6`](https://github.com/Kitware/trame/commit/f748dd6736e4736365f9f18c00c5846c53f47793))

## v2.0.1 (2022-05-31)
### Fix
* **CI:** Add initial CI with semantic-release ([`a881ffb`](https://github.com/Kitware/trame/commit/a881ffb9232fd2f78e445be4be58dcc112181ff5))
* **tools.app:** Add tool to create html app ([`d8c11e6`](https://github.com/Kitware/trame/commit/d8c11e679500005b976c8e934230aa8ea9f0d072))
* **jupyter:** Proper server.start() call ([`e67625e`](https://github.com/Kitware/trame/commit/e67625e9775f688da7d80d5b2ea97d779af61dfb))
* **tools/www:** Make it server independent ([`1d7ad31`](https://github.com/Kitware/trame/commit/1d7ad3197d445ffd600d5069c993a44c5f831a18))

### Documentation
* **content:** Fix doc wording ([`490196e`](https://github.com/Kitware/trame/commit/490196e62a5252a7b8b50d0b6bda03746d796ce8))
* **example:** Fix RemoteSelection for trame v2 ([`4c2ba6d`](https://github.com/Kitware/trame/commit/4c2ba6d2ebc5c4af0bb6427ecaff0435bf6d4a39))
* **api:** Add missing information ([`32a9a4a`](https://github.com/Kitware/trame/commit/32a9a4a47232a24e7c79d3f037cd3c2fad7fcf56))
* **api:** Adding more api doc ([`0c9948d`](https://github.com/Kitware/trame/commit/0c9948d03f4a271747965afe7f68b3889e4c9daa))
* **api:** Adding more api doc ([`a78df91`](https://github.com/Kitware/trame/commit/a78df91235244a6cff4f688298bee91e98df5096))
* **rtd:** Update wwww ([`13258ad`](https://github.com/Kitware/trame/commit/13258ad7e807d18b5fa7123d28b59f452833a114))
* **migration:** Add widgets.html info ([`4e57496`](https://github.com/Kitware/trame/commit/4e5749670935e6ba684289d9f894782a1151c0a8))
* **example:** Add link to v1-v2 delta ([`b28723d`](https://github.com/Kitware/trame/commit/b28723d7e9ea56006e230b1898f3d158f77f49d6))
* **example:** Add missing v2 migration ([`7b3cda7`](https://github.com/Kitware/trame/commit/7b3cda7c45b8a60132892f762e16ed28cb709481))
* **website:** Update landing page ([`faba163`](https://github.com/Kitware/trame/commit/faba16314dc229be1b9991fb8b3108d3d94a81a9))
* **examples:** Add ref to v1 + delta ([`c9bc9dc`](https://github.com/Kitware/trame/commit/c9bc9dc80d14c23782c246e3c202d89ffeed3f95))
* **website:** Update content to match new api ([`5f55d6a`](https://github.com/Kitware/trame/commit/5f55d6a575d3fb6afb28d49adc66e7f1afb22d96))
* **examples:** Update and cleanup examples for v2 ([`e8ad216`](https://github.com/Kitware/trame/commit/e8ad2164e64ab1656516f399afed639413ee5421))

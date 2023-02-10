# Gitlab CI/CD

1. **.gitlab-ci.yml**
```yml
# https://docs.gitlab.cn/14.0/ee/ci/yaml/README.html
# https://docs.gitlab.com/ee/ci/variables/predefined_variables.html

include:
  - local: /gitlab-ci/build.yml
  - local: /gitlab-ci/code-quality.yml
  - local: /gitlab-ci/mr-notification.yml
```    
2. **code-quality.yml** 
```yml
lint_debug:
  image: cimg/android:2022.04-node
  stage: build
  only:
    - merge_requests
  script:
    - ./gradlew lintDebug
  interruptible: true

detekt:
  image: cimg/android:2022.04-node
  stage: build
  only:
    - merge_requests
  script:
    - ./gradlew detekt
  interruptible: true
```
3. **build.yml**
```
before_script:
  - echo keyalias=hello > local.properties
  - echo storepassword=world >> local.properties
  - echo keypassword=world >> local.properties

  - echo nexus.user= >> local.properties
  - echo nexus.password= >> local.properties
  - echo maven.url= >> local.properties

build_debug_Google:
  image: cimg/android:2022.04-node
  stage: build
  only:
    - merge_requests
  script:
    - ./gradlew :sample:assembleGoogleDebug
  artifacts:
    name: "build-debug-google"
    #    expose_as: "Build Google Debug"
    paths:
      - sample/build/outputs/apk/googleIap/debug/msdk_demo_*_*-google-iap-debug.apk
    expire_in: 2 weeks
  interruptible: true
  
build_release_Google:
  image: cimg/android:2022.04-node
  stage: build
  only:
    - merge_requests
  script:
    - ./gradlew :sample:assembleGoogleRelease
  artifacts:
    name: "build-release-google"
    #    expose_as: "Build Google Release"
    paths:
      - sample/build/outputs/apk/googleIap/release/msdk_demo_*_*-google-iap-release.apk
      - sample/build/outputs/mapping/googleIapRelease/mapping.txt
    expire_in: 2 weeks
  interruptible: true

```
4. **参考资料**
* [使用GitLab实现ci/cd](https://zhuanlan.zhihu.com/p/136843588)
* [搞定yml文件.yml文件基本用法汇总](https://zhuanlan.zhihu.com/p/493137181)
  
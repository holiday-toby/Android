# Gradle中依赖传递与aar打包发布
## 参考文档
1. [基于本地仓库搭建nexus私服](https://blog.csdn.net/ac_dao_di/article/details/121888447)
2. [gradle设置允许maven仓库使用http url](https://docs.gradle.org/7.4/dsl/org.gradle.api.artifacts.repositories.UrlArtifactRepository.html#org.gradle.api.artifacts.repositories.UrlArtifactRepository:allowInsecureProtocol)
3. [Maven学习六之利用mvn deploy命令上传包](https://developer.aliyun.com/article/444176)
4. [手动上传jar包到远程仓库 (maven deploy)](https://www.cnblogs.com/pekkle/p/10373506.html)
5. [使用mvn deploy:deploy-file 上传jar/pom至nexus私服](https://blog.csdn.net/yanglee365/article/details/103046511)

## 依赖jar/aar文件
1. 需要添加flatDir标签，将lib所在的目录标记为仓库
2. 使用lib.aar
3. 项目根目录的build.gradle文件中，暴露子module的libs文件夹
```gradle
allprojects {
    repositories {
        jcenter()
        google()
        mavenCentral()
        maven { url 'https://developer.huawei.com/repo/' }

        flatDir {
            dirs project(':login-line').file('libs')
        }
//
//        maven {
//            url "http://localhost:8081/repository/maven-public/"
//            allowInsecureProtocol true
//        }
    }
}
```
setting文件中可指明project的根目录
```
include ':login-line'
project(':login-line').projectDir = file('login/login-line')
```
使用lib文件
```
dependencies {
    implementation fileTree(include: ['*.jar'], dir:'libs')

    implementation(name: 'line-sdk-4.0.6', ext: 'aar')
    
//  implementation 'com.linecorp:line-sdk:4.0.6'
}
```

## 发布到本地maven仓库
直接依赖jar文件，在对外发布的时候是不利的。因为对外发布的aar包中不包含jar中的代码，就会提示找不到
```gradle

afterEvaluate {
    def moduleName = project.name
    def versionName = rootProject.ext.msdk.versionName + rootProject.ext.msdk.versionSuffix

    publishing {
        publications {
            debug(MavenPublication) {
                from components.debug
                groupId = rootProject.ext.msdk.groupId
                artifactId = moduleName
                version = versionName
            }
        }
        repositories {
            maven {
                def props = new Properties()
                props.load(project.rootProject.file("local.properties").newDataInputStream())

                def baseRepoUrl = props.get("maven.url")
                if (baseRepoUrl == null) throw new GradleException("maven.url not found in local.properties")

//                def releasesRepoUrl = "$baseRepoUrl/releases"
//                def snapshotsRepoUrl = "$baseRepoUrl/snapshots"
//                url = versionName.endsWith('SNAPSHOT') ? snapshotsRepoUrl : releasesRepoUrl
                url = baseRepoUrl
                allowInsecureProtocol = true //支持http
                credentials {
                    username = props.get("nexus.user")
                    password = props.get("nexus.password")
                }
            }
        }
    }
}

```
local.properties
```
sdk.dir=/Users/duanhao.ling/Library/Android/sdk
maven.url=http://localhost:8081/repository/maven-snapshots/
nexus.user=toby
nexus.password=admin

```

## 使用maven命令上传jar包
1. ```brew install maven```
2. 需要在/usr/local/Cellar/maven/3.8.7/libexec/conf/setting目录下配置servers
```
<servers>
    <server>
        <id>maven-snapshots</id>
        <username>toby</username>
        <password>admin</password>
    </server>
    <server>
        <id>thirdparty</id>
        <username>toby</username>
        <password>admin</password>
    </server>
</servers>
```
3. mvn使用install命令上传到本地maven仓库，使用deploy命令将jar包上传到远程仓库
- 注意repositoryId为url最后一段，需要保持一致。
- 在没有子依赖的情况下可以自动生成pom文件，`-Dfile=line-sdk-4.0.6.aar -Dpackaging=aar -DgeneratePom=true`。
- 如果aar/jar存在子依赖，必须同时上传pom文件，`-Dfile=twitter-core-3.3.0.aar -Dpackaging=aar -DgeneratePom=fasle `禁止自动生成pom，因为无法覆盖上传。
- 上传多个文件时,多次执行mvn deploy:deploy-file命令,修改这两个参数即可,例如`-Dfile=twitter-core-3.3.0.pom -Dpackaging=pom`。类似上传doc以及source文件。
```
➜ ~ mvn deploy:deploy-file -DgroupId=com.linecorp.linesdk -DartifactId=linesdk -Dpackaging=aar -DgeneratePom=true -DrepositoryId=thirdparty -Dfile=line-sdk-4.0.6.aar -Durl=http://localhost:8081/repository/thirdparty -Dversion=4.0.6 -DallowInsecureProtocol=true -X

# 上传line-sdk到garenanow
➜ ~ mvn deploy:deploy-file -Durl=https://maven.garenanow.com/nexus/content/repositories/releases -DrepositoryId=releases -Dversion=4.0.6 -DgroupId=com.linecorp -DartifactId=line-sdk -Dpackaging=aar -DgeneratePom=true  -Dfile=line-sdk-4.0.6.aar -X

# 上传twitter-core aar
➜ ~ mvn deploy:deploy-file -DgeneratePom=fasle  -DgroupId=com.twitter.sdk.android -DartifactId=twitter-core  -Dversion=3.3.0 -DPomFile=twitter-core-3.3.0.pom -Dfile=twitter-core-3.3.0.aar -Dpackaging=aar -DrepositoryId=thirdparty -Durl=http://localhost:8081/repository/thirdparty -DallowInsecureProtocol=true -X
# 上传twitter-core pom文件
➜ ~ mvn deploy:deploy-file -DgeneratePom=fasle  -DgroupId=com.twitter.sdk.android -DartifactId=twitter-core  -Dversion=3.3.0 -DPomFile=twitter-core-3.3.0.pom -Dfile=twitter-core-3.3.0.pom -Dpackaging=pom -DrepositoryId=thirdparty -Durl=http://localhost:8081/repository/thirdparty -DallowInsecureProtocol=true -X

➜ ~ mvn deploy:deploy-file -DgeneratePom=fasle  -DgroupId=com.twitter.sdk.android -DartifactId=twitter-core  -Dversion=3.3.0 -DPomFile=twitter-core-3.3.0.pom -Dfile=twitter-core-3.3.0.pom -Dpackaging=pom -Durl=https://maven.garenanow.com/nexus/content/repositories/releases -DrepositoryId=releases -DallowInsecureProtocol=true -X
```
## 上传jar包之后，切换不同的仓库加载同一个依赖Gradle提示不匹配
```
Caused by: org.gradle.api.internal.artifacts.transform.TransformException: Failed to transform hwid-5.3.0.302.aar (com.huawei.hms:hwid:5.3.0.302) to match attributes {artifactType=android-aar-metadata, org.gradle.category=library, org.gradle.libraryelements=jar, org.gradle.status=release, org.gradle.usage=java-runtime}.
```
这个时候除了需要删除该库本地的缓存，还要删除本地缓存的目录metadata
解决方案
```
➜  modules-2 pwd
/Users/duanhao.ling/.gradle/caches/modules-2
➜  modules-2 find ./ -name "com.huawei.hms"
.//metadata-2.97/descriptors/com.huawei.hms
.//files-2.1/com.huawei.hms
➜  modules-2 rm -rf .//metadata-2.97/descriptors/com.huawei.hms
➜  modules-2 rm -rf ./files-2.1/com.huawei.hms
➜  modules-2 find ./ -name "com.huawei.hms"
```
## 另一种依赖链问题解决方案
适合该仓库中存在大量互相依赖的特有库，一一上传就不太方便了。如果是不断更新的文件，这样上传特定版本也无法及时收到版本更新提醒。

可以在nexus服务中添加proxy仓库，并在public group仓库设置中配置优先级进行公开
![](image/截屏2023-02-08%20下午4.39.48.png)

## 管理员账号权限
1. 创建与管理仓库
2. web页面中上传与删除库 
3. 远程上传到thirdparty仓库需要管理员账号

## 默认仓库对应地址
- Google() https://maven.google.com/web/index.html
- MavenLocal() ~/.m2/repository/目录
- MavenCentral()
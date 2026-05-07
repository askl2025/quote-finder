[app]

title = 名句匹配
package.name = quotefinder
package.domain = com.quotefinder
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

requirements = python3,kivy,requests,urllib3,certifi,charset-normalizer,idna

[buildozer]
log_level = 2
warn_on_root = 0

[app]

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.release_artifact = apk
android.gradle_dependencies =
android.add_activities =
android.gradle_repositories =
android.accept_sdk_license = True

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

[app.gradle_dependencies]

[app.gradle_repositories]

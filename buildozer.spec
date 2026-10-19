[app]
title = Code Editor
package.name = codeeditor
package.domain = org.example
source.dir = .
source.include_exts = py,kv,txt
version = 1.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0
android.api = 35
android.minapi = 23
android.ndk = 27c
android.archs = armeabi-v7a, arm64-v8a
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
# Kivy uses SDL2 and OpenGL ES through python-for-android.
# Optional video playback dependency (requires a compatible p4a recipe):
# requirements = python3,kivy,pyjnius,ffpyplayer
# ffmpeg is not bundled as a standalone dependency here.

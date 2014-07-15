#! /bin/sh

TOTAL=0
EXTRACTED=0
for ZIP_FILE in zips/android*.zip; do
  ((TOTAL++))
  APK_FILE=$(echo $ZIP_FILE | sed "s/android/ContentShell/;s/zip/apk/g")
  if [ ! -f $APK_FILE ]; then
    echo "Extracting $APK_FILE..."
    unzip -p $ZIP_FILE chrome-android/apks/ContentShell.apk > $APK_FILE
    ((EXTRACTED++))
  fi
done
echo "Extracted $EXTRACTED out of $TOTAL APK files"

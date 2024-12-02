Sezon ve episode bilgisine bakarak, srt altyazı dosyalarını film isimleri ile aynı yapar.
Varsayılan olarak .mkv dosyaları, varsayılan dil kodu ise tr dir.

## Örnek Kullanım:

Sadece dil kodu:
```bash
python sub.py "/path/to/folder" en
```
Bu durumda dil kodu en olarak alınır.


Hem uzantı hem de dil kodu:  
```bash
python sub.py "/path/to/folder" .mp4,.mkv en
```
Varsayılan dil kodu:  
```bash
python sub.py "/path/to/folder"
```

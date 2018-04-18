The Dapeng Binary Downloader
======================
![Alt text](http://p6wf2jj0b.bkt.clouddn.com/dapeng_log.jpg)

First you need to install
----------------------

	pip install beautifulsoup4
	pip install lxml

How to use the script
----------------------

1. Open cmd in the script path.
2. use the command:

```
    python DP_Bin_Downloader.py <request_id>
```


The <font color="#3A5FCD"><request_id></font> is the part of the red box in the picture.

![Alt text](http://p6wf2jj0b.bkt.clouddn.com/request_id.PNG)

3. Then the script will ask you if download all binaries.You need to input 'y' or 'n'.
If you input 'n', the script will only download one page (up to 20) binaries.
4. The out files are saved at <font color="#3A5FCD"><script_path>/binary/<request_id></font>.



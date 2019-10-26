# Linux Kernel Assistance Tool (KAT)

## Introduce

![wide](https://user-images.githubusercontent.com/24751868/67603138-0b29b480-
f7b3-11e9-97f8-f9faead83de7.PNG)

**This project is tested from linux kernel v5.0.2.**

KAT help you to develop and analyze linux kernel code conveniently.
KAT provide **File tree**, **Tag list**, **Explorer** for you.
1. File tree
    - ![filetree](https://user-images.githubusercontent.com/24751868/67603135-
0a911e00-f7b3-11e9-8a90-2ebdc841d155.PNG)
    - It show you files which will be compiled probably.
1. Tag list
    - ![taglist](https://user-images.githubusercontent.com/24751868/67603137-
0b29b480-f7b3-11e9-9f99-90601075f02e.PNG)
    - It show you tags in current window.
1. Explorer
    - ![explorer](https://user-images.githubusercontent.com/24751868/67603132-
0a911e00-f7b3-11e9-9c66-91715dc127da.PNG)
    - It show you tag's definitions if you put a mapped key.


KAT's objective is many people use linux kernel source code usefully and
conveniently in various environments which is to be used various text editors
and IDEs through local and remote accesses.
Currently, It is developed for only linux kernel. But perhaps it'll be improved
to provide useful development environment with various IDEs and text editors for
many projects containing linux kernel. (I call it **Plug-in Development
Environment**)


## Install

### Preceding condition

I don't prepare auto installer yet. Please do as follows first.

1. linux/Makefile
	- Append `kat` into `no-dot-config-targets`
	``` makefile
	no-dot-config-targets := clean mrproper distclean \
					   cscope gtags TAGS tags help% %docs check% coccicheck \
					   $(version_h) headers_% archheaders archscripts \
					   kernelversion %src-pkg \
					   kat
	```

	- Append `kat.ref` into `MRPROPER_FILES`
	``` makefile
	MRPROPER_FILES += .config .config.old .version \
				  Module.symvers tags TAGS cscope* GPATH GTAGS GRTAGS GSYMS \
				  signing_key.pem signing_key.priv signing_key.x509   \
				  x509.genkey extra_certificates signing_key.x509.keyid     \
				  signing_key.x509.signer vmlinux-gdb.py \
				  kat.ref
	```

	- Append the following line into `help:`
	``` makefile
		@echo  '  kat             - Generate kat file for editors'
	```

	- Append the `kat` into following block
	``` makefile
	tags TAGS cscope gtags kat: FORCE
		$(call cmd,tags)
	```

1. linux/scripts/tags.sh
	- Append function definition `dokat()` between all\_kconfigs() and docscope()
	``` sh
	dokat()
	{
		  (echo ":options:"; \
		  echo ":files:"; \
		  all_target_sources; \
		  echo ":kconfigs:"; \
		  all_kconfigs) > kat.ref

	}
	```

    - Append caller of `dokat` into case scope
    ``` sh
	case "$1" in
		"cscope")
			docscope
			;;

		"gtags")
			dogtags
			;;

		"tags")
			rm -f tags
			xtags ctags
			remove_structs=y
			;;

		"TAGS")
			rm -f TAGS
			xtags etags
			remove_structs=y
			;;

	#################### Append under text ######################
		"kat")
			# ignore sound and drivers
			ignore="$ignore ( -path ${tree}drivers ) -prune -o"
			ignore="$ignore ( -path ${tree}sound ) -prune -o"
			dokat
			;;
	#############################################################
	esac
	```

### Download KAT


#### Vundle

Append **Vundle** plugin in `.vimrc`.
If you don't know **Vundle** you can visit [here][Vundle] in order to use.

``` vim
Plugin 'tot0rokr/kat'
```

and install.

``` vim
:PluginInstall
```


## Use

First, you should make `kat.ref` from `Makefile` where `$PWD` are in linux
directory.

``` sh
$ make kat
$ make ARCH=$(ARCH) kat		# make ARCH=arm64 kat
```

Second, execute `Vim`.

``` sh
$ vim
```

and, you could see loading and making kat.database which is in order to be fast
loading.

- ![loading](https://user-images.githubusercontent.com/24751868/67620993-5f7e7
400-f847-11e9-8191-b9c4d48e1681.PNG)



### Set Variable

You can customize variables if you want.

|Variable|Default|Description|
|:-------|:-----:|:----------|
|g:KATUsing|1(True)|0(False) is not using KAT. Otherwise(True), KAT is used|
|g:KATUsingFileTree|1(True)|0(False) is not using Filetree. Otherwise, used|
|g:KATUsingTagList|1(True)|0(False) is not using Taglist. Otherwise, used|
|g:KATUsingExplorer|1(True)|0(False) is not using Explorer. Otherwise, used|
|g:KATCreateDefaultMappings|1(True)|If this value is 0(False), don't use default key-mapping|
|g:KATSizeFileTree|30|Filetree's window width size|
|g:KATSizeTagList|30|Taglist's window width size|
|g:KATSizeExplorer|8|Explorer's window height size|


### Set Command and Key-mapping

You can customize command key-mapping.

#### Global

|Target|Default|Description|
|:-----|:-----:|:----------|
|\<Plug\>KATAttachFileTree|\-|Open the Filetree window|
|\<Plug\>KATDetachFileTree|\-|Close the Filetree window|
|\<Plug\>KATToggleFileTree|\\]f|Toggle the Filetree window|
|\<Plug\>KATAttachTagList|\-|Open the Taglist window|
|\<Plug\>KATDetachTagList|\-|Close the Taglist window|
|\<Plug\>KATToggleTagList|\\]t|Toggle the Taglist window|
|\<Plug\>KATAttachExplorer|\-|Open the Explorer window|
|\<Plug\>KATDetachExplorer|\-|Close the Explorer window|
|\<Plug\>KATToggleExplorer|\\]e|Toggle the Explorer window|
|\<Plug\>KATShowTagExplorer|\\]s|Open the Explorer window and show Tag definition under the cursor|


#### Filetree

|Target|Default|Description|
|:-----|:-----:|:----------|
|\<Plug\>KATFileOpenFileTree|\<Enter\>|Open a file under the cursor|

Filetree's abbreviations is shown in Filetree by pushing `?`


#### Taglist

|Target|Default|Description|
|:-----|:-----:|:----------|
|\<Plug\>KATGotoTagList|\<Enter\>|Go to a Tag under the cursor|

Taglist's abbreviations is shown in Taglist by pushing `?`

#### Explorer

|Target|Default|Description|
|:-----|:-----:|:----------|
|\<Plug\>KATGotoTagExplorer|\<C-]\> and g]|Open a file which a Tag under the cursor in, and go to the tag|
|\<Plug\>KATSelectTagExplorer|\<Enter\>|If found tags is multiple, you can choose one by pushing Key|







[Vundle]: https://github.com/VundleVim/Vundle.vim

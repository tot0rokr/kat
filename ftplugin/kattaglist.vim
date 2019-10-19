if exists("b:current_filetype_plugin")
    finish
endif
let b:current_filetype_plugin = g:KATFiletypeTagList

setlocal nowrap

nnoremap <buffer> q     :hide<CR>|" quit
" nmap <buffer> <C-]>     <Plug>KATGotoTagExplorer|" goto tag what is shown by Explorer
" nmap <buffer> g]        <Plug>KATGotoTagExplorer|" goto tag what is shown by Explorer
" nmap <buffer> <leader>g <Plug>KATGotoTagExplorer|" goto tag what is shown by Explorer
nmap <buffer> <Enter>   <Plug>KATGotoTagList|" if tag is matched Explorer
" show matched tag list, then you can choose one by using 'KATSelectTagExplorer' command

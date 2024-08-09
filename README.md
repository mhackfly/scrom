## scrom

**Description**

`Scrom` is an application that allows you to download ROMs for various emulation systems.
These ROMs are retrieved from [Archive.org](https://archive.org), a site that references
numerous consoles, platforms, and applications related to emulation.
This application was developed in Python with the GTK3 graphical library.
The Bash script `scrom.sh` launches the application and manages the addition of new systems.
It scans the `/links` directory for new `.dat` files. These data files contain the system name,
uploader ID, file extension, and system pages. The pages are scanned for ROM download links.
Finally, these links are inserted into a database.
The names of the data files correspond to the system name associated with the uploader ID.  

Example : `links/dreamcast_retrogamechampion.dat` :

```
dreamcast
retrogamechampion
zip
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/1/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/4/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/9/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/A/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/B/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/C/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/D/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/E/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/F/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/G/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/H/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/I/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/J/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/K/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/L/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/M/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/N/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/O/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/P/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/Q/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/R/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/S/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/T/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/U/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/V/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/W/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/X/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/Y/
https://archive.org/download/sega-dreamcast-champion-collection-updated-v2/Z/
```

Example : `links/megadrive_ic3dragon5110.dat` :

```
megadrive
ic3dragon5110
zip
https://ia804709.us.archive.org/view_archive.php?archive=/31/items/megadrive_202212/megadrive.zip
```

Example : `links/ps3_cvlt_of_mirrors.dat`

```
ps3
cvlt_of_mirrors
iso
https://archive.org/download/sony_playstation3_numberssymbols
https://archive.org/download/sony_playstation3_a_part1
https://archive.org/download/sony_playstation3_a_part2
https://archive.org/download/sony_playstation3_a_part3
https://archive.org/download/sony_playstation3_b_part1
https://archive.org/download/sony_playstation3_b_part2
https://archive.org/download/sony_playstation3_b_part3
https://archive.org/download/sony_playstation3_c_part1
https://archive.org/download/sony_playstation3_c_part2
https://archive.org/download/sony_playstation3_c_part3
https://archive.org/download/sony_playstation3_d_part1
https://archive.org/download/sony_playstation3_d_part2
https://archive.org/download/sony_playstation3_d_part3
https://archive.org/download/sony_playstation3_d_part4
https://archive.org/download/sony_playstation3_d_part5
https://archive.org/download/sony_playstation3_e
https://archive.org/download/sony_playstation3_f_part1
https://archive.org/download/sony_playstation3_f_part2
https://archive.org/download/sony_playstation3_f_part3
https://archive.org/download/sony_playstation3_g_part1
https://archive.org/download/sony_playstation3_g_part2
https://archive.org/download/sony_playstation3_g_part3
https://archive.org/download/sony_playstation3_h_part1
https://archive.org/download/sony_playstation3_h_part2
https://archive.org/download/sony_playstation3_i
https://archive.org/download/sony_playstation3_j
https://archive.org/download/sony_playstation3_k
https://archive.org/download/sony_playstation3_l_part1
https://archive.org/download/sony_playstation3_l_part2
https://archive.org/download/sony_playstation3_l_part3
https://archive.org/download/sony_playstation3_m_part1
https://archive.org/download/sony_playstation3_m_part2
https://archive.org/download/sony_playstation3_m_part3
https://archive.org/download/sony_playstation3_m_part4
https://archive.org/download/sony_playstation3_m_part5
https://archive.org/download/sony_playstation3_n_part1
https://archive.org/download/sony_playstation3_n_part2
https://archive.org/download/sony_playstation3_n_part3
https://archive.org/download/sony_playstation3_o_part1
https://archive.org/download/sony_playstation3_o_part2
https://archive.org/download/sony_playstation3_o_part3
https://archive.org/download/sony_playstation3_p_part1
https://archive.org/download/sony_playstation3_p_part2
https://archive.org/download/sony_playstation3_q
https://archive.org/download/sony_playstation3_r_part1
https://archive.org/download/sony_playstation3_r_part2
https://archive.org/download/sony_playstation3_r_part3
https://archive.org/download/sony_playstation3_r_part4
https://archive.org/download/sony_playstation3_s_part1
https://archive.org/download/sony_playstation3_s_part2
https://archive.org/download/sony_playstation3_s_part3
https://archive.org/download/sony_playstation3_s_part4
https://archive.org/download/sony_playstation3_s_part5
https://archive.org/download/sony_playstation3_s_part6
https://archive.org/download/sony_playstation3_t_part1
https://archive.org/download/sony_playstation3_t_part2
https://archive.org/download/sony_playstation3_t_part3
https://archive.org/download/sony_playstation3_t_part4
https://archive.org/download/sony_playstation3_u_part1
https://archive.org/download/sony_playstation3_u_part2
https://archive.org/download/sony_playstation3_v
https://archive.org/download/sony_playstation3_w_part1
https://archive.org/download/sony_playstation3_w_part2
https://archive.org/download/sony_playstation3_x
https://archive.org/download/sony_playstation3_y
https://archive.org/download/sony_playstation3_z
```

**Dependencies**

[sqlite3](https://www.sqlite.org/index.html) : a C library that provides functions for manipulating SQLite databases.  
[curl](https://curl.haxx.se/) : a command-line library that allows you to use communication protocols on the Internet, such as HTTP.  
[lynx](http://lynx.browser.org/) : a text-based web browser that allows you to navigate the Internet in a terminal environment.  
[axel](https://github.com/axel-download-accelerator/axel) : a fast download tool that allows you to download files from the Internet.  

**Usage**

Once in the `scrom` directory, simply execute `./start.sh`.


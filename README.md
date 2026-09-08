# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Julius2342/pyvlx/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                        |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|---------------------------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pyvlx/api/activate\_scene.py                                            |       15 |        7 |        2 |        0 |     47% |19-20, 24-26, 30-31 |
| src/pyvlx/api/api\_event.py                                                 |       36 |       20 |        4 |        0 |     40% |31-60, 69, 73, 77, 81-82 |
| src/pyvlx/api/completable\_api\_event.py                                    |       25 |        1 |        6 |        0 |     97% |        64 |
| src/pyvlx/api/factory\_default.py                                           |       17 |        9 |        2 |        0 |     42% |18-20, 24-28, 32 |
| src/pyvlx/api/frame\_creation.py                                            |      142 |        6 |      130 |        5 |     96% |81-86, 98, 100, 102, 246 |
| src/pyvlx/api/frames/frame\_node\_state\_position\_changed\_notification.py |       47 |        1 |        0 |        0 |     98% |        62 |
| src/pyvlx/api/frames/frame\_status\_request.py                              |      116 |        6 |       16 |        5 |     92% |41, 136-137, 159, 164, 173 |
| src/pyvlx/api/frames/frame\_wink\_send.py                                   |       71 |        2 |        6 |        2 |     95% |    34, 57 |
| src/pyvlx/api/get\_all\_nodes\_information.py                               |       24 |       16 |        8 |        0 |     25% |24-27, 31-44, 48 |
| src/pyvlx/api/get\_local\_time.py                                           |       17 |        9 |        2 |        0 |     42% |18-20, 24-29, 33 |
| src/pyvlx/api/get\_network\_setup.py                                        |       17 |        9 |        2 |        0 |     42% |18-20, 24-29, 33 |
| src/pyvlx/api/get\_node\_information.py                                     |       19 |       12 |        4 |        0 |     30% |16-19, 23-36, 40 |
| src/pyvlx/api/get\_protocol\_version.py                                     |       20 |       10 |        2 |        0 |     45% |19-21, 25-29, 33, 38 |
| src/pyvlx/api/get\_scene\_list.py                                           |       28 |       20 |       10 |        0 |     21% |18-21, 25-43, 47 |
| src/pyvlx/api/get\_state.py                                                 |       17 |        9 |        2 |        0 |     42% |18-20, 24-28, 32 |
| src/pyvlx/api/get\_version.py                                               |       17 |        9 |        2 |        0 |     42% |18-20, 24-29, 33 |
| src/pyvlx/api/house\_status\_monitor.py                                     |       25 |       14 |        4 |        0 |     38% |22-23, 27-30, 34, 42-43, 47-50, 54 |
| src/pyvlx/api/leave\_learn\_state.py                                        |       17 |        9 |        2 |        0 |     42% |18-20, 24-28, 32 |
| src/pyvlx/api/password\_enter.py                                            |       20 |       12 |        6 |        0 |     31% |18-20, 24-33, 37 |
| src/pyvlx/api/reboot.py                                                     |       17 |        9 |        2 |        0 |     42% |18-20, 24-28, 32 |
| src/pyvlx/api/set\_node\_name.py                                            |       16 |        9 |        2 |        0 |     39% |16-19, 23-26, 30 |
| src/pyvlx/api/status\_request.py                                            |       22 |       14 |        4 |        0 |     31% |17-21, 25-38, 42-43 |
| src/pyvlx/api/wink\_send.py                                                 |       19 |        2 |        2 |        0 |     90% |     44-45 |
| src/pyvlx/connection.py                                                     |      129 |       37 |       18 |        1 |     67% |25-27, 31, 35-36, 54, 58-68, 72-73, 152-154, 162, 170, 174, 178, 182-186, 198-202, 206 |
| src/pyvlx/const.py                                                          |      479 |        7 |        2 |        1 |     98% |313, 582, 635, 654, 667, 681, 696 |
| src/pyvlx/dataobjects.py                                                    |       67 |       20 |        8 |        4 |     68% |13-\>15, 15-\>17, 29, 53, 70-73, 77, 88-89, 93, 101-102, 106, 118-121, 125, 136, 140 |
| src/pyvlx/dimmable\_device.py                                               |       21 |        5 |        0 |        0 |     76% |41-48, 58, 71 |
| src/pyvlx/discovery.py                                                      |       56 |       41 |       10 |        0 |     23% |24-28, 36-38, 43-76, 93-98 |
| src/pyvlx/heartbeat.py                                                      |       63 |        9 |       16 |        1 |     87% |30-38, 48-\>50 |
| src/pyvlx/klf200gateway.py                                                  |      108 |       74 |       28 |        0 |     25% |46, 50, 54-55, 59-64, 68-73, 77-82, 86-91, 95-99, 103-107, 112, 117-121, 125-129, 133-138, 142-147, 151-155, 159-165, 169 |
| src/pyvlx/node.py                                                           |       63 |       14 |       14 |        3 |     75% |43, 55, 60, 76, 87-91, 95-96, 100-106, 111 |
| src/pyvlx/node\_updater.py                                                  |      181 |        0 |       90 |        2 |     99% |374-\>381, 383-\>387 |
| src/pyvlx/nodes.py                                                          |      111 |       11 |       66 |        8 |     88% |64-68, 110, 117-120, 127, 130, 133, 139, 151, 156-\>154 |
| src/pyvlx/on\_off\_switch.py                                                |       20 |        7 |        0 |        0 |     65% |24-28, 32, 36, 40, 44 |
| src/pyvlx/opening\_device.py                                                |      217 |      100 |       62 |        7 |     44% |67-72, 102, 106-111, 217, 231, 245, 260, 268, 272-289, 293-303, 417-450, 477, 504, 531, 551, 581-598, 607, 615, 623, 691-738, 761, 790, 807 |
| src/pyvlx/parameter.py                                                      |      212 |       13 |       68 |        7 |     91% |111, 113, 115, 117, 162-166, 360, 362, 364, 389 |
| src/pyvlx/pyvlx.py                                                          |       79 |       41 |       10 |        0 |     43% |12-13, 60-76, 80-84, 88, 92-93, 97-98, 102-114, 118, 122, 126-129 |
| src/pyvlx/scenes.py                                                         |       39 |        6 |       20 |        0 |     83% |     56-61 |
| **TOTAL**                                                                   | **4071** |  **600** |  **754** |   **46** | **83%** |           |

45 files skipped due to complete coverage.


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/Julius2342/pyvlx/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/Julius2342/pyvlx/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Julius2342/pyvlx/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/Julius2342/pyvlx/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FJulius2342%2Fpyvlx%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/Julius2342/pyvlx/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.
# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Julius2342/pyvlx/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                        |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|---------------------------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pyvlx/api/activate\_scene.py                                            |       15 |        7 |        2 |        0 |     47% |21-22, 26-28, 32-33 |
| src/pyvlx/api/api\_event.py                                                 |       36 |       20 |        4 |        0 |     40% |31-60, 69, 73, 77, 81-82 |
| src/pyvlx/api/completable\_api\_event.py                                    |       25 |        1 |        6 |        0 |     97% |        64 |
| src/pyvlx/api/factory\_default.py                                           |       17 |        9 |        2 |        0 |     42% |20-22, 26-30, 34 |
| src/pyvlx/api/frame\_creation.py                                            |      143 |        6 |      130 |        5 |     96% |50-55, 67, 69, 71, 215 |
| src/pyvlx/api/frames/frame\_node\_state\_position\_changed\_notification.py |       47 |        1 |        0 |        0 |     98% |        62 |
| src/pyvlx/api/frames/frame\_status\_request.py                              |      117 |       16 |       16 |        7 |     83% |43, 129-133, 138-139, 153-157, 161, 166, 175 |
| src/pyvlx/api/frames/frame\_wink\_send.py                                   |       72 |        2 |        6 |        2 |     95% |    35, 58 |
| src/pyvlx/api/get\_all\_nodes\_information.py                               |       24 |       16 |        8 |        0 |     25% |22-25, 29-42, 46 |
| src/pyvlx/api/get\_local\_time.py                                           |       17 |        9 |        2 |        0 |     42% |19-21, 25-30, 34 |
| src/pyvlx/api/get\_network\_setup.py                                        |       17 |        9 |        2 |        0 |     42% |19-21, 25-30, 34 |
| src/pyvlx/api/get\_node\_information.py                                     |       19 |       12 |        4 |        0 |     30% |18-21, 25-38, 42 |
| src/pyvlx/api/get\_protocol\_version.py                                     |       20 |       10 |        2 |        0 |     45% |21-23, 27-31, 35, 40 |
| src/pyvlx/api/get\_scene\_list.py                                           |       28 |       20 |       10 |        0 |     21% |20-23, 27-45, 49 |
| src/pyvlx/api/get\_state.py                                                 |       17 |        9 |        2 |        0 |     42% |18-20, 24-28, 32 |
| src/pyvlx/api/get\_version.py                                               |       17 |        9 |        2 |        0 |     42% |19-21, 25-30, 34 |
| src/pyvlx/api/house\_status\_monitor.py                                     |       25 |       14 |        4 |        0 |     38% |20-21, 25-28, 32, 40-41, 45-48, 52 |
| src/pyvlx/api/leave\_learn\_state.py                                        |       17 |        9 |        2 |        0 |     42% |19-21, 25-29, 33 |
| src/pyvlx/api/password\_enter.py                                            |       20 |       12 |        6 |        0 |     31% |20-22, 26-35, 39 |
| src/pyvlx/api/reboot.py                                                     |       17 |        9 |        2 |        0 |     42% |19-21, 25-29, 33 |
| src/pyvlx/api/set\_limitation.py                                            |       27 |        1 |        4 |        1 |     94% |        43 |
| src/pyvlx/api/set\_node\_name.py                                            |       16 |        9 |        2 |        0 |     39% |18-21, 25-28, 32 |
| src/pyvlx/api/status\_request.py                                            |       22 |       14 |        4 |        0 |     31% |19-23, 27-40, 44-45 |
| src/pyvlx/api/wink\_send.py                                                 |       19 |        2 |        2 |        0 |     90% |     46-47 |
| src/pyvlx/connection.py                                                     |      121 |       41 |       16 |        2 |     61% |24-26, 30, 34-35, 53, 57-67, 71-72, 106-108, 139-141, 149, 153, 157, 161, 165, 169-173, 185-189, 193 |
| src/pyvlx/const.py                                                          |      479 |        7 |        2 |        1 |     98% |313, 582, 635, 654, 667, 681, 696 |
| src/pyvlx/dataobjects.py                                                    |       68 |       20 |        8 |        4 |     68% |16-\>18, 18-\>20, 32, 56, 73-76, 80, 91-92, 96, 104-105, 109, 121-124, 128, 139, 143 |
| src/pyvlx/dimmable\_device.py                                               |       21 |        5 |        0 |        0 |     76% |41-48, 58, 71 |
| src/pyvlx/discovery.py                                                      |       57 |       40 |       12 |        0 |     25% |25-29, 40, 44-78, 95-100 |
| src/pyvlx/heartbeat.py                                                      |       63 |        9 |       16 |        2 |     86% |31-39, 48-\>52, 50-\>52 |
| src/pyvlx/klf200gateway.py                                                  |      107 |       74 |       28 |        0 |     24% |36, 40, 44-45, 49-54, 58-63, 67-72, 76-81, 85-89, 93-97, 102, 107-111, 115-119, 123-128, 132-137, 141-145, 149-155, 159 |
| src/pyvlx/node.py                                                           |       58 |       12 |       14 |        3 |     76% |40, 52, 57, 73, 84-88, 92-98, 103 |
| src/pyvlx/node\_updater.py                                                  |      126 |        6 |       62 |       13 |     90% |32, 48-49, 64-\>66, 66-\>87, 80-\>82, 82-\>84, 84-\>87, 172-\>175, 178-\>182, 192-193, 204-\>exit, 230, 231-\>exit |
| src/pyvlx/nodes.py                                                          |      110 |       11 |       66 |        8 |     88% |63-67, 109, 116-119, 126, 129, 132, 138, 150, 155-\>153 |
| src/pyvlx/on\_off\_switch.py                                                |       20 |        7 |        0 |        0 |     65% |24-28, 32, 36, 40, 44 |
| src/pyvlx/opening\_device.py                                                |      215 |      100 |       62 |        7 |     44% |69-74, 104, 108-113, 218, 232, 246, 261, 269, 273-290, 294-304, 418-451, 478, 505, 532, 552, 582-599, 608, 616, 624, 692-739, 762, 791, 808 |
| src/pyvlx/parameter.py                                                      |      215 |       13 |       70 |        7 |     92% |114, 116, 118, 120, 165-169, 363, 365, 367, 392 |
| src/pyvlx/pyvlx.py                                                          |       80 |       41 |       10 |        0 |     43% |13-14, 61-77, 81-85, 89, 93-94, 98-99, 103-115, 119, 123, 127-130 |
| src/pyvlx/scenes.py                                                         |       38 |        6 |       20 |        0 |     83% |     55-60 |
| **TOTAL**                                                                   | **4019** |  **618** |  **726** |   **62** | **82%** |           |

44 files skipped due to complete coverage.


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
# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Julius2342/pyvlx/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                    |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------------------------------------------ | -------: | -------: | -------: | -------: | ------: | --------: |
| pyvlx/api/activate\_scene.py                                            |       26 |       18 |       10 |        0 |     22% |23-27, 31-56, 60-61 |
| pyvlx/api/api\_event.py                                                 |       35 |       20 |        4 |        0 |     38% |30-55, 64, 68, 72, 76-77 |
| pyvlx/api/factory\_default.py                                           |       17 |        9 |        2 |        0 |     42% |20-22, 26-30, 34 |
| pyvlx/api/frame\_creation.py                                            |      143 |        6 |      130 |        5 |     96% |50-55, 67, 69, 71, 215 |
| pyvlx/api/frames/frame\_node\_state\_position\_changed\_notification.py |       47 |        1 |        0 |        0 |     98% |        62 |
| pyvlx/api/frames/frame\_status\_request.py                              |      117 |       16 |       16 |        7 |     83% |43, 129-133, 138-139, 153-157, 161, 166, 175 |
| pyvlx/api/frames/frame\_wink\_send.py                                   |       72 |        2 |        6 |        2 |     95% |    35, 58 |
| pyvlx/api/get\_all\_nodes\_information.py                               |       24 |       16 |        8 |        0 |     25% |22-25, 29-42, 46 |
| pyvlx/api/get\_local\_time.py                                           |       17 |        9 |        2 |        0 |     42% |19-21, 25-30, 34 |
| pyvlx/api/get\_network\_setup.py                                        |       17 |        9 |        2 |        0 |     42% |19-21, 25-30, 34 |
| pyvlx/api/get\_node\_information.py                                     |       19 |       12 |        4 |        0 |     30% |18-21, 25-38, 42 |
| pyvlx/api/get\_protocol\_version.py                                     |       20 |       10 |        2 |        0 |     45% |21-23, 27-31, 35, 40 |
| pyvlx/api/get\_scene\_list.py                                           |       28 |       20 |       10 |        0 |     21% |20-23, 27-45, 49 |
| pyvlx/api/get\_state.py                                                 |       24 |       11 |        2 |        0 |     50% |19-21, 25-29, 33, 38, 43 |
| pyvlx/api/get\_version.py                                               |       17 |        9 |        2 |        0 |     42% |19-21, 25-30, 34 |
| pyvlx/api/house\_status\_monitor.py                                     |       25 |       14 |        4 |        0 |     38% |20-21, 25-28, 32, 40-41, 45-48, 52 |
| pyvlx/api/leave\_learn\_state.py                                        |       17 |        9 |        2 |        0 |     42% |19-21, 25-29, 33 |
| pyvlx/api/password\_enter.py                                            |       20 |       12 |        6 |        0 |     31% |20-22, 26-35, 39 |
| pyvlx/api/reboot.py                                                     |       17 |        9 |        2 |        0 |     42% |19-21, 25-29, 33 |
| pyvlx/api/set\_limitation.py                                            |       27 |        1 |        4 |        1 |     94% |        43 |
| pyvlx/api/set\_node\_name.py                                            |       16 |        9 |        2 |        0 |     39% |18-21, 25-28, 32 |
| pyvlx/api/status\_request.py                                            |       22 |       14 |        4 |        0 |     31% |19-23, 27-40, 44-45 |
| pyvlx/api/wink\_send.py                                                 |       32 |        5 |       10 |        1 |     81% |44->47, 56-58, 62-63 |
| pyvlx/connection.py                                                     |      110 |       59 |       16 |        2 |     42% |20, 24-26, 30, 34-35, 47-49, 53, 57-67, 71-72, 99-100, 104-106, 110-127, 135, 139, 143, 147, 151, 155-159, 164-167, 171-176, 180 |
| pyvlx/const.py                                                          |      480 |        7 |        2 |        1 |     98% |319, 597, 652, 673, 686, 700, 715 |
| pyvlx/dataobjects.py                                                    |       68 |       20 |        8 |        4 |     68% |16->18, 18->20, 32, 56, 73-76, 80, 91-92, 96, 104-105, 109, 121-124, 128, 139, 143 |
| pyvlx/dimmable\_device.py                                               |       21 |        5 |        0 |        0 |     76% |41-48, 58, 71 |
| pyvlx/discovery.py                                                      |       57 |       40 |       12 |        0 |     25% |25-29, 40, 44-78, 95-100 |
| pyvlx/heartbeat.py                                                      |       54 |        9 |       10 |        1 |     84% |30-38, 42->44 |
| pyvlx/klf200gateway.py                                                  |      107 |       74 |       28 |        0 |     24% |36, 40, 44-46, 50-55, 59-64, 68-73, 77-82, 86-90, 94-98, 103, 108-112, 116-120, 124-129, 133-138, 142-146, 150-156, 160 |
| pyvlx/node.py                                                           |       40 |       11 |        4 |        1 |     68% |38, 42, 47, 51-55, 59-65, 70 |
| pyvlx/node\_helper.py                                                   |       41 |        4 |       30 |        4 |     89% |50, 74, 100, 109 |
| pyvlx/node\_updater.py                                                  |      126 |        6 |       62 |       13 |     90% |32, 48-49, 64->66, 66->87, 80->82, 82->84, 84->87, 172->175, 178->182, 192-193, 204->exit, 230, 231->exit |
| pyvlx/nodes.py                                                          |       73 |       22 |       46 |        0 |     70% |74-77, 81-90, 94-102 |
| pyvlx/on\_off\_switch.py                                                |       20 |        7 |        0 |        0 |     65% |24-28, 32, 36, 40, 44 |
| pyvlx/opening\_device.py                                                |      222 |      105 |       64 |        7 |     43% |68-73, 95, 99-104, 183, 203, 217, 232, 240, 244-261, 265-275, 329-333, 390-422, 441, 459, 477, 485, 505-521, 530, 537, 544, 601-647, 662, 681, 695 |
| pyvlx/parameter.py                                                      |      214 |       13 |       70 |        7 |     92% |113, 115, 117, 119, 164-168, 362, 364, 366, 391 |
| pyvlx/pyvlx.py                                                          |       80 |       41 |       10 |        0 |     43% |13-14, 61-77, 81-85, 89, 93-94, 98-99, 103-115, 119, 123, 127-130 |
| pyvlx/scene.py                                                          |       17 |        4 |        2 |        0 |     68% |     36-43 |
| pyvlx/scenes.py                                                         |       38 |        6 |       20 |        0 |     83% |     55-60 |
| **TOTAL**                                                               | **3989** |  **674** |  **738** |   **56** | **80%** |           |

42 files skipped due to complete coverage.


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
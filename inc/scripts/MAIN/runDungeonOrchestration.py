import threading
import time
import random
from findObjectInMinimap import FindObjectInMinimap
from findObjectInMinimap import findSpecificItemOnMinimap
from blacksmith import Blacksmith


class RunDungeonOrchestration(threading.Thread):
    def __init__(self, threads, src_window, images_path, dungeon_name, language, send_text_to_bot, from_python, moveplayer, solo):
        threading.Thread.__init__(self)
        self.threads = threads
        self.threads.wait_until_thread_initialized('CaptureWorker')
        self.threads.wait_until_thread_initialized('DungeonWorker')
        self.src_window = src_window
        self.stopped = False
        self.paused = False
        self.dungeon_name = dungeon_name
        self.img_path = images_path
        self.captureWorker = threads.get_thread('CaptureWorker')
        self.fight = threads.get_thread('Fight')
        self.dungeonWorker = threads.get_thread('DungeonWorker')
        self.CheckDungeonTime = threads.get_thread('CheckDungeonTime')
        self.RunDungeonThread = threads.get_thread('RunDungeonThread')
        self.CheckDungeonMandatoryStep = None
        self.language = language
        self.send_text_to_bot = send_text_to_bot
        self.from_python = from_python
        self.follow_player_number = 1
        self.moveplayer = moveplayer
        self.following_player = False
        self.solo = solo
        self.player_is_dead = False
        self.actual_threads_status = None
        self.checkpoint_after_die = None
        self.completely_stopped = False
        self.replay_dungeon = False
        self.found_blacksmith_inside_dungeon = False
        self.special_event = False
        self.blacksmith = Blacksmith(threads, src_window, images_path + '\\'+language+'\\blacksmith',
                                     language, moveplayer, '', '', '', send_text_to_bot, from_python, '', '')
        if not hasattr(self, 'total_runs'):
            self.total_runs = 0

#  STEP TEMPLATE
        # {
        #     "name": "Kill Ongori",
        #     "solo": {
        #         "before_start": {
        #             "executed": False,
        #             "execute_after_die": True,
        #             "model_name": None,
        #             "threads": None,
        #             "feedback": {
        #                 "before_feedback": None,
        #                 "in_progress": None,
        #                 "after_feedback": None
        #             },
        #         },
        #         "in_progress": {
        #             "executed": False,
        #             "execute_after_die": True,
        #             "model_name": None,
        #             "threads": None,
        #             "feedback": {
        #                 "before_feedback": None,
        #                 "in_progress": None,
        #                 "after_feedback": None
        #             },
        #         },
        #         "after_end": {
        #             "executed": False,
        #             "execute_after_die": True,
        #             "model_name": None,
        #             "threads": None,
        #             "feedback": {
        #                 "before_feedback": None,
        #                 "in_progress": None,
        #                 "after_feedback": None
        #             }
        #         },
        #     },
        #     "party": {},
        # }

        self.scenario = {
            "namari": {
                "area_to_hide": [59, 80],
                "steps": [
                    {
                        "name": "Main hall 1",
                        "solo": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": "./models/modelv61__model-modelv61-100-epochs_namariv2_2.h5",
                                "threads": [
                                    {"Fight": False},
                                    {"CheckLoot": False},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": False}
                                ],
                                "feedback": {
                                    "before_feedback": None,
                                    "in_progress": {
                                        "action": "manual_move",
                                        "movements": [
                                            ("↗", 1),
                                        ]
                                    },
                                    "after_feedback": None
                                }
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                    {"Fight": False},
                                    {"CheckLoot": False},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": True}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "wait_time",
                                        "time": 3,
                                        "threads": None
                                    },
                                    "in_progress": {
                                        "action": "wait_time",
                                        "time": 10,
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLoot": False},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False}
                                        ],
                                    },
                                    "after_feedback": {
                                        "action": "wait_to_fight",
                                        "time": 5,
                                        "threads": None
                                    },
                                }
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                            },
                        },
                        "party": {},
                    },
                    {
                        "name": "Main hall 2",
                        "solo": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": False,
                                "threads": [
                                    {"DungeonWorker": False}
                                ],
                                "feedback": None
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": False,
                                "threads": [
                                    {"DungeonWorker": True}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "wait_time",
                                        "time": 3,
                                        "threads": None
                                    },
                                    "in_progress": {
                                        "action": "wait_time",
                                        "time": 10,
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLoot": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False}
                                        ],
                                    },
                                    "after_feedback": {
                                        "action": "wait_to_fight",
                                        "time": 5,
                                        "threads": None
                                    },
                                }
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                            },
                        },
                        "party": {},
                    },
                    {
                        "name": "Main hall to Namari",
                        "solo": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": [
                                    {"Fight": True},
                                    {"CheckLoot": False},
                                    {"CheckLife": False},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": True}
                                ],
                                "feedback": None
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": None,
                                    "in_progress": {
                                        "action": "find_image_and_click",
                                        "path": "\\game_items",
                                        "file": "talk",
                                        "need_found": True,
                                        "coords": (1, 1),
                                        "threads": None
                                    },
                                    "after_feedback": {
                                        "action": "find_image_and_click",
                                        "path": f"\\{self.language}\\dungeons\\namari",
                                        "file": "talk_after",
                                        "need_found": True,
                                        "coords": (0, -142),
                                        "threads": [
                                            {"Fight": False},
                                            {"CheckLoot": False},
                                            {"CheckLife": False},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False}
                                        ]
                                    },
                                }
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": [
                                    {"Fight": True},
                                    {"CheckLoot": False},
                                    {"CheckLife": False},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": False}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\namari",
                                        "file": "namari",
                                        "need_found": True,
                                        "coords": None,
                                        "threads": None,
                                        "wait_to_disappear": True
                                    },
                                    "in_progress": None,
                                    "after_feedback": None
                                }
                            },
                        },
                        "party": {},
                    },
                    {
                        "name": "Namari to middle room",
                        "solo": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": {
                                        "action": "manual_move",
                                        "movements": [
                                            ("↖", 3),
                                        ],
                                        "threads": None
                                    },
                                    "in_progress": {
                                        "action": "wait_time",
                                        "time": 4,
                                        "threads": [
                                            {"Fight": False},
                                            {"CheckLoot": False},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": True}
                                        ]
                                    },
                                    "after_feedback": None
                                }
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": [
                                    {"Fight": True},
                                    {"CheckLoot": False},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": False}
                                ],
                                "feedback": None,
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\namari",
                                        "file": "namari",
                                        "need_found": True,
                                        "coords": None,
                                        "threads": None
                                    },
                                    "in_progress": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\namari",
                                        "file": "namari",
                                        "need_found": False,
                                        "coords": None,
                                        "threads": None
                                    },
                                    "after_feedback": None
                                }
                            }
                        },
                        "party": {},
                    },
                    {
                        "name": "Middle room to last room",
                        "solo": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": [
                                            {"Fight": False},
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "manual_move",
                                        "movements": [
                                            ("↖", 4),
                                        ],
                                    },
                                    "in_progress": {
                                        "action": "wait_time",
                                        "time": 3,
                                        "threads": [
                                            {"Fight": False},
                                            {"CheckLoot": False},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": True}
                                        ]
                                    },
                                },
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": [
                                    {"Fight": True},
                                    {"CheckLoot": False},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": False}
                                ],
                                "feedback": None,
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                            },
                        },
                        "party": {},
                    },
                    {
                        "name": "Last room to boss room",
                        "solo": {
                            "before_start":  {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\namari",
                                        "file": "namari",
                                        "need_found": True,
                                        "coords": None,
                                        "threads": None
                                    },
                                    "in_progress": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\namari",
                                        "file": "namari",
                                        "need_found": False,
                                        "coords": None,
                                        "threads": None
                                    },
                                    "after_feedback": None
                                }
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                    {"Fight": False},
                                    {"CheckLoot": False},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": True}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "manual_move",
                                        "movements": [
                                            ("↗", 1),
                                        ],
                                        "threads": None
                                    },
                                    "in_progress": {
                                        "action": "find_image_and_click",
                                        "path": "\\game_items",
                                        "file": "hand_up",
                                        "need_found": True,
                                        "coords": (1, 1),
                                    },
                                    "after_feedback": None
                                },
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                            },
                        },
                        "party": {},
                    },
                    {
                        "name": "Boss room 1",
                        "solo": {
                            "before_start":  {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": [
                                    {"Fight": False},
                                    {"CheckLoot": False},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": False}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "wait_time",
                                        "time": 5,
                                        "threads": None
                                    },
                                    "in_progress": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\namari",
                                        "file": "before_boss",
                                        "need_found": True,
                                        "coords": (0, -142),
                                        "threads": None
                                    },
                                    "after_feedback": {
                                        "action": "manual_move",
                                        "movements": [
                                            ("↗", 1),
                                        ],
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLoot": False},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False}
                                        ]
                                    },
                                }
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\namari",
                                        "file": "sargoth",
                                        "need_found": True,
                                        "coords": None,
                                        "wait_to_disappear": True,
                                        "threads": None
                                    },
                                    "in_progress": None,
                                    "after_feedback": None
                                }
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\namari",
                                        "file": "sargoth",
                                        "need_found": True,
                                        "coords": None,
                                        "wait_to_disappear": True,
                                        "threads": None
                                    },
                                    "in_progress": None,
                                    "after_feedback": None
                                }
                            }
                        },
                        "party": {},
                    }
                ]
            },
            "kikuras": {
                "area_to_hide": [54, 79],
                "steps": [
                    {
                        "name": "0 - To the Raft",
                        "solo": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                    {"Fight": True},
                                    {"CheckLoot": False},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": False}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "model_name": self.img_path + "\\..\\data\\models\\common_model1.dat",
                                    },
                                    "in_progress": {
                                        "action": "manual_move",
                                        "movements": [
                                            ("↘", 1),
                                            ("→", 1),
                                        ],
                                    },
                                    "after_feedback": {
                                        "threads": [
                                            {"DungeonWorker": True},
                                            {"Fight": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"CheckDungeonLoot": True}
                                        ],
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "reach_the_river",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 35,
                                        "action_if_timeout": [
                                            {
                                                "action": "manual_move",
                                                "movements": [
                                                    ("↖", 1),
                                                    ("↘", 1),
                                                    ("→", 1),
                                                ]
                                            },
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "before_start",
                                                "feedback": "after_feedback"
                                            }
                                        ]
                                    }
                                },
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                    {"Fight": True},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": True}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": "\\game_items",
                                        "file": "hand_up",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 10,
                                        "action_if_timeout": [
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "before_start",
                                                "feedback": "after_feedback"
                                            }
                                        ],
                                    },
                                    "in_progress": {
                                        "action": "wait_to_fight",
                                        "time": 5,
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False}
                                        ]
                                    },
                                    "after_feedback": None,
                                },
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": True}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image_and_click",
                                        "path": "\\game_items",
                                        "file": "hand_up",
                                        "need_found": True,
                                        "timeout": 5,
                                        "coords": (1, 1),
                                        "action_if_timeout": [
                                            {
                                                "action": "manual_move",
                                                "movements": [
                                                    ("↖", 1),
                                                    ("↘", 1),
                                                    ("→", 2),
                                                ]
                                            },
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "before_start",
                                                "feedback": "in_progress"
                                            }
                                        ]
                                    },
                                    "in_progress": {
                                        "action": "find_image",
                                        "path": "\\game_items",
                                        "file": "hand_up",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 10,
                                        "threads": None,
                                        "wait_to_disappear": True,
                                        "action_if_timeout": [
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "before_start",
                                                "feedback": "after_feedback"
                                            }
                                        ]
                                    },
                                    "after_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "board_the_raft",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 15,
                                        "action_if_timeout": [
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "before_start",
                                                "feedback": "after_feedback"
                                            }
                                        ],
                                        "threads": [
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"Fight": False},
                                        ]
                                    },
                                }
                            },
                        },
                        "party": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                    {"Fight": False},
                                    {"CheckLoot": False},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": False}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "model_name": self.img_path + "\\..\\data\\models\\common_model1.dat",
                                    },
                                    "in_progress": {
                                        "action": "manual_move",
                                        "movements": [
                                            ("↘", 1),
                                            ("→", 1),
                                        ],
                                    },
                                    "after_feedback": {
                                        "threads": [
                                            {"DungeonWorker": True},
                                            {"Fight": False},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"CheckDungeonLoot": True}
                                        ],
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "reach_the_river",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 35,
                                        "action_if_timeout": [
                                            {
                                                "action": "manual_move",
                                                "movements": [
                                                    ("↖", 1),
                                                    ("↘", 1),
                                                    ("→", 1),
                                                ]
                                            },
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "before_start",
                                                "feedback": "after_feedback"
                                            }
                                        ]
                                    }
                                },
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                    {"Fight": False},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": True}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": "\\game_items",
                                        "file": "hand_up",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 10,
                                        "action_if_timeout": [
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "in_progress",
                                                "feedback": "before_feedback"
                                            }
                                        ],
                                    },
                                    "in_progress": {
                                        "action": "wait_to_fight",
                                        "time": 5,
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False}
                                        ]
                                    },
                                    "after_feedback": None,
                                },
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": True}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image_and_click",
                                        "path": "\\game_items",
                                        "file": "hand_up",
                                        "need_found": True,
                                        "timeout": 5,
                                        "coords": (1, 1),
                                        "action_if_timeout": [
                                            {
                                                "action": "manual_move",
                                                "movements": [
                                                    ("↖", 1),
                                                    ("↘", 1),
                                                    ("→", 2),
                                                ]
                                            },
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "before_start",
                                                "feedback": "in_progress"
                                            }
                                        ]
                                    },
                                    "in_progress": {
                                        "action": "find_image",
                                        "path": "\\game_items",
                                        "file": "hand_up",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 10,
                                        "threads": None,
                                        "wait_to_disappear": True,
                                        "action_if_timeout": [
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "before_start",
                                                "feedback": "after_feedback"
                                            }
                                        ]
                                    },
                                    "after_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "board_the_raft",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 15,
                                        "action_if_timeout": [
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "after_end",
                                                "feedback": "after_feedback"
                                            }
                                        ],
                                        "threads": [
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"Fight": False},
                                            {"DungeonWorker": True},
                                        ]
                                    },
                                }
                            },
                        },
                    },
                    {
                        "name": "1 - Raft for Kikuras",
                        "solo": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "feedback": {
                                    "before_feedback": {
                                        "action": "manual_move",
                                        "movements": [
                                            ("↘", 2),
                                        ]
                                    },
                                    "in_progress": {
                                        "threads": [
                                            {"Fight": True},
                                            {"DungeonWorker": False},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"CheckLoot": True},
                                        ],
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "ride_the_raft_into_the_jungle",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 10,
                                        "action_if_timeout": [
                                            {
                                                "action": "manual_move",
                                                "movements": [
                                                    ("↖", 1),
                                                    ("↘", 1),
                                                    ("→", 2),
                                                ]
                                            },
                                        ]
                                    },
                                    "after_feedback": {
                                        "checkpoint_after_die": True,
                                        "action": "wait_time",
                                        "time": 60,
                                        "threads": None
                                    }
                                },
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "survive_the_fire",
                                        "need_found": True,
                                        "coords": None,
                                    },
                                    "in_progress": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "ride_the_raft_into_the_jungle",
                                        "need_found": True,
                                        "coords": None,
                                    },
                                    "after_feedback": {
                                        "checkpoint_after_die": True,
                                        "action": "wait_time",
                                        "time": 55,
                                    }
                                },
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                    {"CheckLoot": True},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": True}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "find_boss",
                                        "need_found": True,
                                        "coords": None,
                                    },
                                    "in_progress": {
                                        "checkpoint_after_die": True,
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLoot": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": True}
                                        ],
                                    },
                                    "after_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "kill_ongori",
                                        "need_found": True,
                                        "coords": None,
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLoot": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": True}
                                        ]
                                    }
                                }
                            },
                        },
                        "party": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "feedback": {
                                    "before_feedback": None,
                                    "in_progress": {
                                        "threads": [
                                            {"Fight": True},
                                            {"DungeonWorker": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"CheckLoot": False},
                                        ],
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "ride_the_raft_into_the_jungle",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 10,
                                        "action_if_timeout": [
                                            {
                                                "action": "go_to_step",
                                                "step_num": 1,
                                                "step_part": "before_start",
                                                "feedback": "before_feedback"
                                            },
                                        ]
                                    },
                                    "after_feedback": {
                                        "checkpoint_after_die": True,
                                        "action": "wait_time",
                                        "time": 60,
                                        "threads": [
                                            {"Fight": True},
                                            {"DungeonWorker": False},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"CheckLoot": False},
                                        ]
                                    }
                                },
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "survive_the_fire",
                                        "need_found": True,
                                        "coords": None,
                                    },
                                    "in_progress": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "ride_the_raft_into_the_jungle",
                                        "need_found": True,
                                        "coords": None,
                                    },
                                    "after_feedback": {
                                        "checkpoint_after_die": True,
                                        "action": "wait_time",
                                        "time": 55,
                                    }
                                },
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                    {"CheckLoot": True},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"DungeonWorker": True}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "find_boss",
                                        "need_found": True,
                                        "coords": None,
                                    },
                                    "in_progress": {
                                        "checkpoint_after_die": True,
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLoot": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": True}
                                        ],
                                    },
                                    "after_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\kikuras",
                                        "file": "kill_ongori",
                                        "need_found": True,
                                        "coords": None,
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLoot": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": True}
                                        ]
                                    }
                                }
                            },
                        },
                    },
                    {
                        "name": "2 - Kill Ongori",
                        "solo": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                            {"Fight": True},
                                            {"CheckLoot": False},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_item_on_screen",
                                        "itemName": "boss",
                                        "timeout": 5,
                                        "approximate": True,
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLoot": False},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False}
                                        ]
                                    },
                                    "in_progress": None,
                                    "after_feedback": {
                                        "action": "find_image",
                                        "path": "\\game_items",
                                        "file": "closing_dungeon",
                                        "need_found": True,
                                        "coords": None,
                                        "threads": None,
                                        "timeout": 5,
                                        "action_if_timeout": [
                                            {
                                                "action": "manual_move",
                                                "movements": [
                                                    ("→", 2),
                                                    ("↗", 3),
                                                ]
                                            },
                                            {
                                                "action": "go_to_step",
                                                "step_num": 2,
                                                "step_part": "before_start",
                                                "feedback": "before_feedback"
                                            }
                                        ]
                                    },
                                },
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": {
                                        "set_timer": 180,
                                        "threads": [
                                            {"DungeonWorker": False},
                                            {"Fight": False},
                                            {"CheckLoot": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                        ],
                                        "action": "wait_time",
                                        "time": 5,
                                    },
                                    "in_progress": {
                                        "threads": [
                                            {"DungeonWorker": False},
                                            {"Fight": False},
                                            {"CheckLoot": False},
                                            {"CheckLife": False},
                                            {"CheckIsDead": False},
                                            {"CheckDungeonLoot": True},
                                        ],
                                        "action": "find_item_on_screen",
                                        "itemName": "blacksmith",
                                        "timeout": 6,
                                        "approximate": True,
                                        "wait_to_disappear": False,
                                        "time_to_wait_to_disappear": None,
                                        "path": "\\game_items",
                                        "feedback_image": "talk",
                                    },
                                    "after_feedback": {
                                        "threads": [
                                            {"DungeonWorker": False},
                                            {"Fight": False},
                                            {"CheckLoot": False},
                                            {"CheckLife": False},
                                            {"CheckIsDead": False},
                                            {"CheckDungeonLoot": True},
                                        ],
                                        "action": "manual_move",
                                        "movements": [
                                            ("→", 2),
                                            ("↗", 1),
                                        ],
                                    }
                                },
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                            {"DungeonWorker": False},
                                            {"Fight": False},
                                            {"CheckLoot": False},
                                            {"CheckLife": False},
                                            {"CheckIsDead": False},
                                            {"CheckDungeonLoot": False},
                                        ],
                                "feedback": {
                                    "before_feedback": {
                                        "threads": [
                                            {"DungeonWorker": False},
                                            {"Fight": False},
                                            {"CheckLoot": False},
                                            {"CheckLife": False},
                                            {"CheckIsDead": False},
                                            {"CheckDungeonLoot": False},
                                        ],
                                        "action": "find_item_on_screen",
                                        "itemName": "exit_portal",
                                        "timeout": 6,
                                        "approximate": True,
                                        "wait_to_disappear": False,
                                        "time_to_wait_to_disappear": None,
                                        "path": "\\game_items",
                                        "feedback_image": "portal",
                                        "action_if_timeout": [
                                            {
                                                "action": "exit_dungeon",
                                            }
                                        ],
                                    },
                                    "in_progress": {
                                        "threads": [
                                            {"DungeonWorker": False},
                                            {"Fight": False},
                                            {"CheckLoot": False},
                                            {"CheckLife": False},
                                            {"CheckIsDead": False},
                                            {"CheckDungeonLoot": False},
                                        ],
                                    },
                                    "after_feedback": {
                                        "threads": [
                                            {"DungeonWorker": False},
                                            {"Fight": False},
                                            {"CheckLoot": False},
                                            {"CheckLife": False},
                                            {"CheckIsDead": False},
                                            {"CheckDungeonLoot": False},
                                        ],
                                    }
                                }
                            },
                        },
                        "party": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": [
                                            {"Fight": True},
                                            {"CheckLoot": False},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_item_on_screen",
                                        "itemName": "boss",
                                        "timeout": 5,
                                        "approximate": True,
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLoot": False},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False}
                                        ]
                                    },
                                    "in_progress": None,
                                    "after_feedback": {
                                        "action": "find_image",
                                        "path": "\\game_items",
                                        "file": "closing_dungeon",
                                        "need_found": True,
                                        "coords": None,
                                        "threads": None,
                                        "timeout": 5,
                                        "action_if_timeout": [
                                            {
                                                "action": "manual_move",
                                                "movements": [
                                                    ("→", 2),
                                                    ("↗", 3),
                                                ]
                                            },
                                            {
                                                "action": "go_to_step",
                                                "step_num": 2,
                                                "step_part": "before_start",
                                                "feedback": "before_feedback"
                                            }
                                        ]
                                    },
                                },
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": {
                                        "set_timer": 180,
                                        "threads": [
                                            {"DungeonWorker": False},
                                            {"Fight": False},
                                            {"CheckLoot": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                        ],
                                        "action": "wait_time",
                                        "time": 5,
                                    },
                                    "in_progress": {
                                        "threads": [
                                            {"DungeonWorker": False},
                                            {"Fight": False},
                                            {"CheckLoot": False},
                                            {"CheckLife": False},
                                            {"CheckIsDead": False},
                                        ],
                                        "action": "find_item_on_screen",
                                        "itemName": "blacksmith",
                                        "timeout": 6,
                                        "approximate": True,
                                        "wait_to_disappear": False,
                                        "time_to_wait_to_disappear": None,
                                        "path": "\\game_items",
                                        "feedback_image": "talk",
                                    },
                                    "after_feedback": {
                                        "action": "manual_move",
                                        "movements": [
                                            ("→", 2),
                                            ("↗", 1),
                                        ],
                                    }
                                },
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": True,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_item_on_screen",
                                        "itemName": "exit_portal",
                                        "timeout": 6,
                                        "approximate": True,
                                        "wait_to_disappear": False,
                                        "time_to_wait_to_disappear": None,
                                        "path": "\\game_items",
                                        "feedback_image": "portal",
                                        "action_if_timeout": [
                                            {
                                                "action": "exit_dungeon",
                                            }
                                        ],
                                    },
                                    "in_progress": None,
                                    "after_feedback": None
                                }
                            },
                        },
                    },
                ]
            },
            "king_breach": {
                "area_to_hide": [54, 79],
                "steps": [
                    {
                        "name": "0 - King Breach floot 1",
                        "solo": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": self.img_path + "\\..\\data\\models\\king_breach.dat",
                                "threads": [
                                    {"Fight": True},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"CheckLoot": False},
                                    {"DungeonWorker": False}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "manual_move",
                                        "movements": [
                                            ("↗", 4),
                                        ]
                                    },
                                    "in_progress": {
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"CheckLoot": False},
                                            {"DungeonWorker": False}
                                        ],
                                        "action": "wait_to_fight",
                                        "time": 3,
                                    },
                                    "after_feedback": {
                                        "threads": [
                                            {"Fight": True},
                                            {"DungeonWorker": False},
                                        ],
                                        "action": "manual_move",
                                        "movements": [
                                            ("↗", 3),
                                        ]
                                    },
                                },
                            },
                            "in_progress": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": None,
                                "feedback": {
                                    "before_feedback": {
                                        "threads": [
                                            {"Fight": True},
                                            {"DungeonWorker": False},
                                        ],
                                        "action": "wait_time",
                                        "time": 3,
                                    },
                                    "in_progress": {
                                        "threads": [
                                            {"Fight": True},
                                            {"DungeonWorker": True},
                                        ],
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\king_breach",
                                        "file": "defeat_sir_gorash",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 4,
                                        "action_if_timeout": [
                                            {
                                                "action": "manual_move",
                                                "movements": [
                                                    ("↙", 4),
                                                ]
                                            },
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "in_progress",
                                                "feedback": "in_progress"
                                            },
                                        ]
                                    },
                                    "after_feedback": {
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False},
                                        ],
                                        "action": "find_item_on_screen",
                                        "itemName": "boss",
                                        "timeout": 5,
                                        "approximate": True,
                                    },
                                },
                            },
                            "after_end": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": [
                                    {"Fight": True},
                                    {"CheckLife": True},
                                    {"CheckIsDead": True},
                                    {"CheckLoot": True},
                                    {"DungeonWorker": True}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "find_image",
                                        "path": f"\\{self.language}\\dungeons\\king_breach",
                                        "file": "interact_portal",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 10,
                                        "action_if_timeout": [
                                            {
                                                "action": "go_to_step",
                                                "step_num": 0,
                                                "step_part": "in_progress",
                                                "feedback": "after_feedback"
                                            },
                                        ]
                                    },
                                    "in_progress": {
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLife": True},
                                            {"CheckIsDead": True},
                                            {"CheckLoot": True},
                                            {"DungeonWorker": True}
                                        ],
                                        "action": "find_image",
                                        "path": "\\game_items",
                                        "file": "hand_up",
                                        "need_found": True,
                                        "coords": None,
                                        "timeout": 10,
                                    },
                                    "after_feedback": {
                                        "threads": [
                                            {"Fight": True},
                                            {"CheckLife": False},
                                            {"CheckIsDead": True},
                                            {"DungeonWorker": False},
                                        ],
                                        "action": "find_image_and_click",
                                        "path": "\\game_items",
                                        "file": "hand_up",
                                        "need_found": True,
                                        "timeout": 5,
                                        "coords": (1, 1),
                                    },
                                }
                            },
                        },
                        "party": {},
                    },
                    {
                        "name": "1 - King Breach floot 2 TMP",
                        "solo": {
                            "before_start": {
                                "executed": False,
                                "execute_after_die": False,
                                "model_name": None,
                                "threads": [
                                    {"Fight": False},
                                    {"CheckLife": False},
                                    {"CheckIsDead": False},
                                    {"CheckLoot": False},
                                    {"DungeonWorker": False}
                                ],
                                "feedback": {
                                    "before_feedback": {
                                        "action": "wait_time",
                                        "time": 20,
                                    },
                                    "in_progress": {
                                        "action": "exit_dungeon",
                                    },
                                },
                            }
                        },
                        "party": {},
                    },
                    # {
                    #     "name": "1 - Second Floor",
                    #     "solo": {
                    #         "before_start": {
                    #             "executed": False,
                    #             "execute_after_die": False,
                    #             "model_name": None,
                    #             "threads": [
                    #                 {"Fight": True},
                    #                 {"CheckLife": True},
                    #                 {"CheckIsDead": True},
                    #                 {"CheckLoot": True},
                    #                 {"DungeonWorker": True}
                    #             ],
                    #             "feedback": {
                    #                 "before_feedback": {
                    #                     "threads": None,
                    #                     "action": "find_image",
                    #                     "path": f"\\{self.language}\\dungeons\\king_breach",
                    #                     "file": "reach_courtyard",
                    #                     "need_found": True,
                    #                     "coords": None,
                    #                     "timeout": 30,
                    #                     "action_if_timeout": [
                    #                         {
                    #                             "action": "go_to_step",
                    #                             "step_num": 0,
                    #                             "step_part": "after_end",
                    #                             "feedback": "before_feedback"
                    #                         },
                    #                     ]
                    #                 },
                    #                 "in_progress": {
                    #                     "checkpoint_after_die": True,
                    #                     "threads": [
                    #                         {"Fight": True},
                    #                         {"CheckLife": True},
                    #                         {"CheckIsDead": True},
                    #                         {"CheckLoot": True},
                    #                         {"DungeonWorker": True}
                    #                     ],
                    #                     "action": "find_image",
                    #                     "path": f"\\{self.language}\\dungeons\\king_breach",
                    #                     "file": "defeat_undead_guardians",
                    #                     "need_found": True,
                    #                     "coords": None,
                    #                     "timeout": 50,
                    #                     "action_if_timeout": [
                    #                         {
                    #                             "action": "go_to_step",
                    #                             "step_num": 1,
                    #                             "step_part": "before_start",
                    #                             "feedback": "in_progress"
                    #                         },
                    #                     ]
                    #                 },
                    #                 "after_feedback": {
                    #                     "threads": [
                    #                         {"Fight": True},
                    #                         {"CheckLife": True},
                    #                         {"CheckIsDead": True},
                    #                         {"DungeonWorker": True},
                    #                     ],
                    #                     "action": "find_image",
                    #                     "path": f"\\{self.language}\\dungeons\\king_breach",
                    #                     "file": "defeat_manoruk",
                    #                     "need_found": True,
                    #                     "coords": None,
                    #                     "timeout": 6,
                    #                     "action_if_timeout": [
                    #                         {
                    #                             "action": "manual_move",
                    #                             "movements": [
                    #                                 # top-left
                    #                                 ("↗", 2),
                    #                                 ("↙", 2),
                    #                             ]
                    #                         },
                    #                         {
                    #                             "action": "go_to_step",
                    #                             "step_num": 1,
                    #                             "step_part": "before_start",
                    #                             "feedback": "in_progress"
                    #                         },
                    #                     ]
                    #                 },
                    #             }
                    #         },
                    #         "in_progress": {
                    #             "executed": False,
                    #             "execute_after_die": False,
                    #             "model_name": None,
                    #             "threads": [
                    #                 {"Fight": True},
                    #                 {"CheckLife": True},
                    #                 {"CheckIsDead": True},
                    #                 {"CheckLoot": True},
                    #                 {"DungeonWorker": True}
                    #             ],
                    #             "feedback": {
                    #                 "before_feedback": {
                    #                     "threads": [
                    #                         {"Fight": True},
                    #                         {"CheckLife": True},
                    #                         {"CheckIsDead": True},
                    #                         {"DungeonWorker": False},
                    #                     ],
                    #                     "action": "find_item_on_screen",
                    #                     "itemName": "boss",
                    #                     "timeout": 5,
                    #                     "approximate": True,
                    #                 },
                    #                 "in_progress": {
                    #                     "action": "find_image",
                    #                     "path": f"\\{self.language}\\dungeons\\king_breach",
                    #                     "file": "enter_the_portal",
                    #                     "need_found": True,
                    #                     "coords": None,
                    #                     "timeout": 10,
                    #                     "threads": [
                    #                         {"Fight": True},
                    #                         {"CheckLife": True},
                    #                         {"CheckIsDead": True},
                    #                         {"CheckLoot": True},
                    #                         {"DungeonWorker": True}
                    #                     ],
                    #                     "action_if_timeout": [
                    #                         {
                    #                             "action": "manual_move",
                    #                             "movements": [
                    #                                 ("↙", 4),
                    #                             ]
                    #                         },
                    #                         {
                    #                             "action": "go_to_step",
                    #                             "step_num": 2,
                    #                             "step_part": "before_start",
                    #                             "feedback": "after_feedback"
                    #                         },
                    #                     ]
                    #                 },
                    #                 "after_feedback": {
                    #                     "action": "find_image",
                    #                     "path": "\\game_items",
                    #                     "file": "hand_up",
                    #                     "need_found": True,
                    #                     "coords": None,
                    #                     "timeout": 10,
                    #                     "threads": [
                    #                         {"Fight": True},
                    #                         {"CheckLife": True},
                    #                         {"CheckIsDead": True},
                    #                         {"CheckLoot": True},
                    #                         {"DungeonWorker": True}
                    #                     ],
                    #                     "action_if_timeout": [
                    #                         {
                    #                             "action": "manual_move",
                    #                             "movements": [
                    #                                 ("↙", 4),
                    #                             ]
                    #                         },
                    #                         {
                    #                             "action": "go_to_step",
                    #                             "step_num": 2,
                    #                             "step_part": "in_progress",
                    #                             "feedback": "before_feedback"
                    #                         },
                    #                     ]
                    #                 },
                    #             }
                    #         },
                    #         "after_end": {
                    #             "executed": False,
                    #             "execute_after_die": False,
                    #             "model_name": None,
                    #             "threads": [
                    #                 {"Fight": True},
                    #                 {"CheckLife": True},
                    #                 {"CheckIsDead": True},
                    #                 {"CheckLoot": True},
                    #                 {"DungeonWorker": True}
                    #             ],
                    #             "feedback": {
                    #                 "before_feedback": {
                    #                     "threads": [
                    #                         {"Fight": True},
                    #                         {"CheckLife": False},
                    #                         {"CheckIsDead": True},
                    #                         {"DungeonWorker": False},
                    #                     ],
                    #                     "action": "find_image_and_click",
                    #                     "path": "\\game_items",
                    #                     "file": "hand_up",
                    #                     "need_found": True,
                    #                     "timeout": 5,
                    #                     "coords": (1, 1),
                    #                     "action_if_timeout": [
                    #                         {
                    #                             "action": "go_to_step",
                    #                             "step_num": 2,
                    #                             "step_part": "in_progress",
                    #                             "feedback": "before_feedback"
                    #                         },
                    #                     ]
                    #                 },
                    #             },
                    #             "in_progress": None,
                    #             "after_feedback": None
                    #         },
                    #     },
                    #     "party": {},
                    # },
                    # {
                    #     "name": "2 - Third Floor",
                    #     "solo": {
                    #         "before_start": {
                    #             "executed": False,
                    #             "execute_after_die": False,
                    #             "model_name": None,
                    #             "threads": None,
                    #             "feedback": {
                    #                 "before_feedback": {
                    #                     "action": "find_image",
                    #                     "path": f"\\{self.language}\\dungeons\\king_breach",
                    #                     "file": "ascend_the_stairs",
                    #                     "need_found": True,
                    #                     "coords": None,
                    #                     "timeout": 10,
                    #                     "action_if_timeout": [
                    #                         {
                    #                             "action": "go_to_step",
                    #                             "step_num": 2,
                    #                             "step_part": "before_start",
                    #                             "feedback": "before_feedback"
                    #                         },
                    #                     ]
                    #                 },
                    #                 "in_progress": {
                    #                     "threads": [
                    #                         {"Fight": True},
                    #                         {"CheckLife": True},
                    #                         {"CheckIsDead": True},
                    #                         {"CheckLoot": True},
                    #                         {"DungeonWorker": True}
                    #                     ],
                    #                     "checkpoint_after_die": True,
                    #                     "action": "find_image",
                    #                     "path": f"\\{self.language}\\dungeons\\king_breach",
                    #                     "file": "reach_leoric_throne",
                    #                     "need_found": True,
                    #                     "coords": None,
                    #                     "timeout": 30,
                    #                     "action_if_timeout": [
                    #                         {
                    #                             "action": "manual_move",
                    #                             "movements": [
                    #                                 ("↘", 5),
                    #                                 ("↙", 3),
                    #                             ]
                    #                         },
                    #                         {
                    #                             "action": "go_to_step",
                    #                             "step_num": 2,
                    #                             "step_part": "before_start",
                    #                             "feedback": "before_feedback"
                    #                         },
                    #                     ]
                    #                 },
                    #                 "after_feedback": {
                    #                     "threads": [
                    #                         {"Fight": True},
                    #                         {"CheckLife": True},
                    #                         {"CheckIsDead": True},
                    #                         {"CheckLoot": True},
                    #                         {"DungeonWorker": False}
                    #                     ],
                    #                     "action": "find_image",
                    #                     "path": f"\\{self.language}\\dungeons\\king_breach",
                    #                     "file": "clear_the_throne_room",
                    #                     "need_found": True,
                    #                     "coords": None,
                    #                     "timeout": 10,
                    #                     "action_if_timeout": [
                    #                         {
                    #                             "action": "manual_move",
                    #                             "movements": [
                    #                                 # circle
                    #                                 ("↘", 1),
                    #                                 ("↙", 1),
                    #                                 ("↖", 1),
                    #                                 ("↗", 1),
                    #                             ]
                    #                         },
                    #                         {
                    #                             "action": "go_to_step",
                    #                             "step_num": 2,
                    #                             "step_part": "before_start",
                    #                             "feedback": "in_progress"
                    #                         },
                    #                     ]
                    #                 }
                    #             },
                    #         },
                    #         "in_progress": {
                    #             "executed": False,
                    #             "execute_after_die": False,
                    #             "model_name": None,
                    #             "threads": None,
                    #             "feedback": {
                    #                 "before_feedback": None,
                    #                 "in_progress": None,
                    #                 "after_feedback": None
                    #             },
                    #         },
                    #         "after_end": {
                    #             "executed": False,
                    #             "execute_after_die": False,
                    #             "model_name": None,
                    #             "threads": None,
                    #             "feedback": {
                    #                 "before_feedback": None,
                    #                 "in_progress": None,
                    #                 "after_feedback": None
                    #             },
                    #         },
                    #     },
                    #     "party": {},
                    # }
                ]
            }
        }

        self.dungeon_imagesRDO = {
            "kikuras": {
                "solo": (
                    [{
                        "path": f"\\{self.language}\\dungeons\\kikuras",
                        "file": "find_boss",
                        "action": "go_to_step",
                        "step_num": 1,
                        "step_part": "after_end",
                        "feedback": "before_feedback"
                    }],
                    [{
                        "path": f"\\{self.language}\\dungeons\\kikuras",
                        "file": "kill_ongori",
                        "action": "go_to_step",
                        "step_num": 1,
                        "step_part": "after_end",
                        "feedback": "after_feedback"
                    }],
                ),
                "party": (
                    [{
                        "path": f"\\{self.language}\\dungeons\\kikuras",
                        "file": "board_the_raft",
                        "action": "go_to_step",
                        "step_num": 0,
                        "step_part": "after_end",
                        "feedback": "after_feedback"
                    }],
                    [{
                        "path": f"\\{self.language}\\dungeons\\kikuras",
                        "file": "find_boss",
                        "action": "go_to_step",
                        "step_num": 1,
                        "step_part": "after_end",
                        "feedback": "before_feedback"
                    }],
                    [{
                        "path": "\\game_items",
                        "file": "closing_dungeon",
                        "action": "go_to_step",
                        "step_num": 1,
                        "step_part": "after_end",
                        "feedback": "before_feedback"
                    }]
                )
            }
        }

        self.actual_step = 0
        self.actual_step_part = None
        self.actual_step_feedback = None
        self.force_step_part = None
        self.force_step_feedback = None
        self.return_to_old_step = False

    def pause(self):
        self.paused = True

    def stop(self):
        self.stopped = True

    def resume(self):
        self.paused = False

    def run(self):
        print("DEBUG: RunDungeonOrchestration started")
        self.CheckDungeonTime.actual_time = 0
        if not hasattr(self.CheckDungeonTime, 'tmp_dungeon_over_time'):
            self.CheckDungeonTime.tmp_dungeon_over_time = self.CheckDungeonTime.dungeon_over_time
        else:
            if self.CheckDungeonTime.dungeon_over_time != self.CheckDungeonTime.tmp_dungeon_over_time:
                self.CheckDungeonTime.dungeon_over_time = self.CheckDungeonTime.tmp_dungeon_over_time
        self.found_blacksmith_inside_dungeon = False
        while self.stopped is False:
            if self.paused is True:
                self.completely_stopped = True
                time.sleep(1)
                continue
        # try:
            self.completely_stopped = False
            self.fight.set_survivor_mode(True)
            self.threads.resume_thread('CheckDungeonTime')
            self.CheckDungeonMandatoryStep = self.threads.get_thread(
                'CheckDungeonMandatoryStep')
            self.threads.resume_thread('CheckDungeonMandatoryStep')
            self.dungeonWorker.rectangle = self.scenario[self.dungeon_name]['area_to_hide']
            steps = self.scenario[self.dungeon_name]['steps']
            if self.actual_step < len(steps):
                step = steps[self.actual_step]
                if self.solo is True:
                    this_step = step['solo']
                    self.dungeonWorker.record_movements = True
                else:
                    this_step = step['party']
                print('\033[92m' + step['name'] + '\033[0m')
                # print('\033[92m' + str(self.actual_step) + '\033[0m')
                # print in yellow
                print('\033[93m' + 'DEBUG-DELETE actual_step-----> ' +
                      str(self.actual_step) + '\033[0m')
                if self.checkpoint_after_die is not None and self.actual_step < self.checkpoint_after_die:
                    self.actual_step = self.checkpoint_after_die
                    self.checkpoint_after_die = None
                    print('\033[92m' + 'Checkpoint after die' + '\033[0m')
                    print('\033[92m' + str(self.actual_step) + '\033[0m')
                    continue
                # -------------------------------------
                if self.force_step_part is None:
                    if "before_start" in this_step:
                        if self.paused is True:
                            continue
                        self.actual_step_part = "before_start"
                        self.execute_step(
                            "before_start", this_step, step['name'])
                        if self.return_to_old_step is True:
                            self.return_to_old_step = False
                            continue
                    if "in_progress" in this_step:
                        if self.paused is True:
                            continue
                        self.actual_step_part = "in_progress"
                        self.execute_step(
                            "in_progress", this_step, step['name'])
                        if self.return_to_old_step is True:
                            self.return_to_old_step = False
                            continue
                    if "after_end" in this_step:
                        if self.paused is True:
                            continue
                        self.actual_step_part = "after_end"
                        self.execute_step("after_end", this_step, step['name'])
                        if self.return_to_old_step is True:
                            self.return_to_old_step = False
                            continue
                else:
                    # print DEBUG-DELETE
                    print('\033[94m' + 'DEBUG-DELETE force_step_part-----> ' +
                          self.force_step_part + '\033[0m')
                    print('\033[94m' + 'DEBUG-DELETE force_step_feedback-----> ' +
                          self.force_step_feedback + '\033[0m')
                    if self.force_step_feedback is None:
                        if self.paused is True:
                            continue
                        self.actual_step_part = self.force_step_part
                        self.execute_step(self.force_step_part,
                                          this_step, step['name'])
                        if self.return_to_old_step is True:
                            self.return_to_old_step = False
                            continue
                    else:
                        if self.paused is True:
                            continue
                        self.actual_step_part = self.force_step_part
                        self.actual_step_feedback = self.force_step_feedback
                        # print in purple
                        print('\033[95m' + 'DEBUG-DELETE force_step_feedback-----> ' +
                              self.force_step_feedback + '\033[0m')
                        # print in green
                        print(
                            '\033[92m' + 'DEBUG-DELETE this_step-----> ' + str(this_step) + '\033[0m')
                        # print in purple
                        print(
                            '\033[95m' + 'DEBUG-DELETE stepname-----> ' + str(step['name']) + '\033[0m')
                        # print in green
                        print('\033[92m' + 'DEBUG-DELETE force_step_part-----> ' +
                              str(self.force_step_part) + '\033[0m')

                        # action['step_part'],
                        # self.scenario[self.dungeon_name]['steps'][self.actual_step]['solo'],
                        # self.scenario[self.dungeon_name]['steps'][self.actual_step]['name'],
                        # action['feedback']

                        self.execute_step(
                            self.force_step_part, this_step, step['name'], self.force_step_feedback)
                        if self.return_to_old_step is True:
                            self.return_to_old_step = False
                            continue
                    self.force_step_feedback = None
                    self.force_step_part = None

                self.actual_step += 1
            else:
                self.send_text_to_bot.send('-----> End of scenario',
                                           self.from_python)
                self.total_runs += 1
                self.send_text_to_bot.send('--> ' + str(self.total_runs),
                                           self.from_python, "blue")
                self.CheckDungeonTime.actual_time = 0
                self.setAllStepsToFalse()
                if self.replay_dungeon == True:
                    self.replay_dungeon = False
                    print(
                            '\033[93m' + 'DEBUG: REPLAY DUNGEON' + '\033[0m')
                    self.send_text_to_bot.send(
                            'command|finishdungeonfromxfRD', self.from_python, False, True)
                else:
                    if self.found_blacksmith_inside_dungeon == True:
                        # pritn in yellow
                        print(
                            '\033[93m' + 'DEBUG: found_blacksmith_inside_dungeon == True' + '\033[0m')
                        self.send_text_to_bot.send(
                            'command|finishdungeonfromxf', self.from_python, False, True)
                        
                    else:
                        # pritn in yellow
                        print(
                            '\033[93m' + 'DEBUG: found_blacksmith_inside_dungeon == False' + '\033[0m')
                        self.send_text_to_bot.send(
                            'command|finishdungeonfromxfNF', self.from_python, False, True)
                self.threads.pause_all_threads()
        # except Exception as e:
        #     print("DEBUG: runDungeonOrchestration: " + str(e))
        #     time.sleep(1)
        #     continue
            time.sleep(0.5)

    def execute_step(self, step_type, step, name, feedback_type_input=False):
        # print in red
        print('\033[91m DEBUG-->' + name + ' -- ' + step_type + '\033[0m')
        if step_type in step:
            print('\033[91m DEBUG2-->' + name + ' -- ' + step_type + '\033[0m')
            if self.paused is True:
                return
            print(f'\033[92m{name} -- {step_type}\033[0m')
            if self.execute_this_step(step[step_type]['execute_after_die']):
                if feedback_type_input is False:
                    if "model_name" in step[step_type] and step[step_type]['model_name']:
                        self.dungeonWorker.load_model(
                            step[step_type]['model_name'])
                if feedback_type_input is False:
                    if "threads" in step[step_type] and step[step_type]['threads']:
                        self.execute_threads(step[step_type]['threads'])
                if "feedback" in step[step_type] and step[step_type]['feedback']:
                    feedback = step[step_type]['feedback']
                    feedback_list = ["before_feedback",
                                     "in_progress", "after_feedback"]
                    if feedback_type_input is not False:
                        index = feedback_list.index(feedback_type_input)
                        next_values = feedback_list[index:]
                        feedback_list = next_values
                    for feedback_type in feedback_list:
                        if feedback_type in feedback and feedback[feedback_type]:
                            self.actual_step_feedback = feedback_type
                            print(
                                f'\033[94m{name} -- {step_type} -- {feedback_type}\033[0m')
                            if "model_name" in feedback[feedback_type] and feedback[feedback_type]['model_name']:
                                self.dungeonWorker.load_model(
                                    feedback[feedback_type]['model_name'])
                            if "threads" in feedback[feedback_type] and feedback[feedback_type]['threads']:
                                self.execute_threads(
                                    feedback[feedback_type]['threads'])
                            if "set_timer" in feedback[feedback_type] and feedback[feedback_type]['set_timer']:
                                self.CheckDungeonTime.dungeon_over_time = feedback[
                                    feedback_type]['set_timer']
                                self.CheckDungeonTime.actual_time = time.time()
                                print('\033[93m' + 'DEBUG: set_timer -> ' +
                                      str(self.CheckDungeonTime.dungeon_over_time) + '\033[0m')
                                self.send_text_to_bot.send(
                                    'DEBUG: set_timer -> ' + str(self.CheckDungeonTime.dungeon_over_time), self.from_python, "yellow")
                            if "action" in feedback[feedback_type] and feedback[feedback_type]['action']:
                                if self.execute_action_father(feedback[feedback_type]) is False:
                                    return
                            if "checkpoint_after_die" in feedback[feedback_type] and feedback[feedback_type]['checkpoint_after_die']:
                                self.checkpoint_after_die = self.actual_step
                    if self.solo is True:
                        self.scenario[self.dungeon_name]['steps'][self.actual_step]['solo'][step_type]['executed'] = True
                    else:
                        self.scenario[self.dungeon_name]['steps'][self.actual_step]['party'][step_type]['executed'] = True

    def execute_action_father(self, feedback):
        return self.execute_action(feedback['action'],
                                   feedback['time'] if "time" in feedback else None,
                                   feedback['coords'] if "coords" in feedback else None,
                                   feedback['path'] if "path" in feedback else None,
                                   feedback['file'] if "file" in feedback else None,
                                   feedback['need_found'] if "need_found" in feedback else None,
                                   feedback['movements'] if "movements" in feedback else None,
                                   feedback['wait_to_disappear'] if "wait_to_disappear" in feedback else None,
                                   feedback['timeout'] if "timeout" in feedback else 30,
                                   feedback['action_if_timeout'] if "action_if_timeout" in feedback else None,
                                   feedback['move_to_object'] if "move_to_object" in feedback else False,
                                   feedback['player_number'] if "player_number" in feedback else None,
                                   feedback['time_to_follow'] if "time_to_follow" in feedback else None,
                                   feedback['approximate'] if "approximate" in feedback else False,
                                   feedback['time_to_wait_to_disappear'] if "time_to_wait_to_disappear" in feedback else None,
                                   feedback['itemName'] if "itemName" in feedback else None,
                                   feedback['feedback_image'] if "feedback_image" in feedback else None,
                                   )

    def execute_action(self, action, time_to_wait=None, coords=None, path=None, file=None, need_found=None, movements=None, wait_to_disappear=False, timeout=30, action_if_timeout=None, move_to_object=False, player_number=None, time_to_follow=5, approximate=False, time_to_wait_to_disappear=None, itemName=None, feedback_image=None):
        if action == 'wait_time':
            for i in range(time_to_wait):
                self.send_text_to_bot.send(
                    'DEBUG: execute_action Waiting. Left ' + str(time_to_wait - i), self.from_python, "purple")
                print('DEBUG: execute_action Waiting. Left' +
                      str(time_to_wait - i))
                if self.paused is True:
                    return False
                time.sleep(1)
        elif action == 'wait_to_fight':
            if time_to_wait is not None:
                for i in range(time_to_wait):
                    if self.paused is True:
                        return False
                    self.send_text_to_bot.send('DEBUG: execute_action Waiting to fight. Left ' +
                                               str(time_to_wait - i), self.from_python, "purple")
                    print('DEBUG: execute_action Waiting to fight. Left' +
                          str(time_to_wait - i))
                    while self.fight.checkFightIsRunning() is True:
                        self.send_text_to_bot.send(
                            'DEBUG: execute_action Waiting to fight', self.from_python, "blue")
                        print('DEBUG: execute_action Waiting to fight')
                        time.sleep(1)
                    time.sleep(1)
            else:
                while self.fight.checkFightIsRunning() is True:
                    self.send_text_to_bot.send(
                        'DEBUG: execute_action Waiting to fight', self.from_python, "blue")
                    print('DEBUG: execute_action Waiting to fight')
                    time.sleep(1)
        elif action == 'manual_move':
            self.send_text_to_bot.send(
                'DEBUG: manual_move ->' + str(movements), self.from_python, "green")
            print('DEBUG: execute_action manual_move' + str(movements))
            relaunch_dungeonWorker = False
            if self.dungeonWorker.paused is False:
                self.dungeonWorker.pause()
                time.sleep(2)
                relaunch_dungeonWorker = True
            for movement in movements:
                if self.paused is True:
                    self.moveplayer.processing_movement_output('NK')
                    return False
                self.moveplayer.processing_movement_output(movement[0])
                time.sleep(movement[1])
            self.moveplayer.processing_movement_output('NK')
            if relaunch_dungeonWorker is True:
                self.dungeonWorker.resume()
        elif action == 'find_image_and_click' or action == 'find_image':
            print('DEBUG: execute_action find_image_and_click', path, file, coords)
            self.send_text_to_bot.send(
                'DEBUG: image-> ' + str(file), self.from_python, "orange")
            feedback_image_coords = self.moveplayer.founfIconInScreen(
                self.img_path + path, file, 0, False, self.captureWorker.screenshot, False)

            if need_found:
                while feedback_image_coords == (0, 0):
                    if self.paused is True:
                        return False
                    feedback_image_coords = self.moveplayer.founfIconInScreen(
                        self.img_path + path, file, 1, False, self.captureWorker.screenshot, False)
                    time.sleep(0.5)
                    self.send_text_to_bot.send(
                        'DEBUG: timeout to find image ' + str(timeout), self.from_python, "purple")
                    print('DEBUG: timeout to find image' + str(timeout))
                    if timeout == 0:
                        print('DEBUG: execute_action Timeout')
                        print('DEBUG: execute_action action_if_timeout',
                              action_if_timeout)
                        if action_if_timeout is not None:
                            self.execute_action_if_timeout(action_if_timeout)
                        return False
                    timeout -= 1
            else:
                while feedback_image_coords != (0, 0):
                    if self.paused is True:
                        return False
                    feedback_image_coords = self.moveplayer.founfIconInScreen(
                        self.img_path + path, file, 2, False, self.captureWorker.screenshot, False)
                    time.sleep(0.5)
                    self.send_text_to_bot.send(
                        'DEBUG: timeout to NOT find image ' + str(timeout), self.from_python, "purple")
                    print('DEBUG: timeout to NOT find image' + str(timeout))
                    if timeout == 0:
                        print('DEBUG: execute_action Timeout')
                        print('DEBUG: execute_action action_if_timeout',
                              action_if_timeout)
                        if action_if_timeout is not None:
                            self.execute_action_if_timeout(action_if_timeout)
                        return False
                    timeout -= 1
            self.threads.pause_thread('DungeonWorker')
            self.moveplayer.processing_movement_output('NK')
            self.moveplayer.processing_movement_output('NK')
            if action == 'find_image_and_click':
                if coords == (1, 1):
                    self.moveplayer.clickOnCoords(feedback_image_coords)
                else:
                    self.moveplayer.clickOnCoords(
                        (feedback_image_coords[0] + coords[0], feedback_image_coords[1] + coords[1]))

            if wait_to_disappear:
                # timeout = 50
                while feedback_image_coords != (0, 0):
                    if self.paused is True:
                        return False
                    feedback_image_coords = self.moveplayer.founfIconInScreen(
                        self.img_path + path, file, 0, False, self.captureWorker.screenshot, False)
                    time.sleep(0.5)
                    self.send_text_to_bot.send(
                        'DEBUG: timeout to check image disappeared ' + str(timeout), self.from_python, "purple")
                    print('DEBUG: timeout to check image disappeared' +
                          str(timeout))
                    if timeout == 0:
                        print('DEBUG: execute_action Timeout')
                        print('DEBUG: execute_action action_if_timeout',
                              action_if_timeout)
                        if action_if_timeout is not None:
                            self.execute_action_if_timeout(action_if_timeout)
                        return False
                    timeout -= 1
        elif action == 'move_to_minimap':
            # FindObjectInMinimap(capture, fight, Moveplayer,
            #         "path\\to\\immortal_xinofarmer\\inc\\img\\game_items", 'minimap_teleport', True, 8)
            resp = FindObjectInMinimap(
                self.captureWorker, self.fight, self.moveplayer, self.img_path + path, file, move_to_object, movements)
            # if resp == (0,0):
            #     return False
        elif action == 'exit_dungeon':
            from_dungeon_orchestration = True
            self.CheckDungeonTime.force_exit_dungeon(
                from_dungeon_orchestration)
            while self.RunDungeonThread.check_if_player_is_in_dungeon(2) is True:
                self.send_text_to_bot.send(
                    'Player is still in dungeon, waiting 5 seconds to check again.', self.from_python, 'red')
                self.CheckDungeonTime.force_exit_dungeon(
                    from_dungeon_orchestration)
                for i in range(5):
                    if self.paused is True:
                        return False
                    self.send_text_to_bot.send(str(
                        5 - i) + ' seconds left to check if player is still in dungeon.', self.from_python, 'purple')
                    time.sleep(1)
        elif action == 'follow_player':
            if player_number == 'random':
                self.follow_player_number = self.follow_player_number + 1
                if self.follow_player_number > 3:
                    self.follow_player_number = 1
            else:
                self.follow_player_number = player_number
            self.follow_player()
            for i in range(time_to_follow):
                if self.paused is True:
                    return False
                self.send_text_to_bot.send(str(
                    time_to_follow - i) + ' seconds left to follow player.', self.from_python, 'purple')
                time.sleep(1)
        elif action == 'find_item_on_screen':

            # while timeout is passed
            foundedItem = False
            tmp_timeout = timeout
            tmp_timeout_feedback = timeout
            movementsBoss = ['→', '↘', '↓',
                                             '↙', '←', '↖', '↑', '↗']

            print('Debug 1')
            print(f'Item: {itemName}, Timeout: {timeout}, Approximate: {approximate}, Wait to disappear: {wait_to_disappear}, Time to wait to disappear: {time_to_wait_to_disappear}')

            if itemName == 'boss':
                dist = 10
            if itemName == 'blacksmith':
                dist = 2
            if itemName == 'exit_portal':
                dist = 2

            while tmp_timeout > 0 and tmp_timeout_feedback > 0:
                if self.paused is True:
                    return False
                movement, distance = findSpecificItemOnMinimap(
                    self.captureWorker.screenshot, itemName, 1, True)

                if movement is not None and distance is not None:
                    print(
                        f'Debug: Item {itemName} found at distance {distance}')
                    if self.paused is True:
                        return False
                    print(f'Debug 2: {movement} {distance} {dist}')
                    bypass=False
                    if feedback_image is not None:
                        print('Debug 33')
                        feedback_image_coords = self.moveplayer.founfIconInScreen(
                            self.img_path + path, feedback_image, 1, False, self.captureWorker.screenshot, False, False, 0.8)
                        if feedback_image_coords != (0, 0):
                            print('Debug 44')
                            bypass=True
                    if bypass is True or (movement is not None and distance > dist and distance <= 70):
                        foundedItem = True
                        if bypass is False:
                            self.moveplayer.processing_movement_output(movement)
                            time.sleep(1)
                            self.moveplayer.processing_movement_output('NK')
                        print('Debug 8')
                        if feedback_image is not None:
                            foundedItem = False
                            print('debug 9')
                            feedback_image_coords = self.moveplayer.founfIconInScreen(
                                self.img_path + path, feedback_image, 1, False, self.captureWorker.screenshot, False, False, 0.8)
                            if feedback_image_coords != (0, 0):
                                foundedItem = True
                                print('debug 10')
                                if itemName == 'blacksmith':
                                    print('debug 11')
                                    # sell stuff--------------------------------------
                                    if self.blacksmith.process_blacksmith_task(True) is False:
                                        self.found_blacksmith_inside_dungeon = False
                                        return True
                                    self.found_blacksmith_inside_dungeon = True
                                if itemName == 'exit_portal':
                                    print('debug 12')
                                    self.moveplayer.clickOnCoords(
                                        feedback_image_coords)
                                    time.sleep(1)
                                    print('debug 13')
                                    # # # # # # # # # # # # # # # # # # self.moveplayer.clickOnCoords((567, 355))
                                    replay_dungeopn_coords = self.moveplayer.founfIconInScreen(
                                        self.img_path + '\\game_items', 'replay_dungeon', 1, False, self.captureWorker.screenshot, False, False, 0.8)
                                    if replay_dungeopn_coords != (0, 0):
                                        self.moveplayer.clickOnCoords(
                                            replay_dungeopn_coords)
                                        time.sleep(2)
                                        replay_dungeon2_coords = self.moveplayer.founfIconInScreen(
                                            self.img_path + '\\game_items', 'replay_dungeon2', 1, False, self.captureWorker.screenshot, False, False, 0.8)
                                        if replay_dungeon2_coords != (0, 0):
                                            self.moveplayer.clickOnCoords(
                                                replay_dungeon2_coords)
                                            time.sleep(3)
                                            self.send_text_to_bot.send('-----> replay dungeon',
                                                                          self.from_python)
                                        else:
                                            self.replay_dungeon = False
                                            return True
                                        self.replay_dungeon = True
                                        return True
                                    else:
                                        self.replay_dungeon = False

                                time.sleep(1)
                                break
                            else:
                                print('debug 14.0')
                                tmp_timeout_feedback -= 1
                                self.send_text_to_bot.send(
                                    'DEBUG: not found ' + feedback_image + '(' + str((tmp_timeout_feedback - timeout) * -1) + '/' + str(timeout) + ')', self.from_python, "red")
                    if movement is not None and distance < 10:
                        if itemName == 'boss':
                            self.fight.force_fight = True
                            # move player ramdomly 1 times
                            self.moveplayer.processing_movement_output(
                                movementsBoss[random.randint(0, 7)])
                            time.sleep(1)
                            self.moveplayer.processing_movement_output('NK')
                        time.sleep(1)
                    if movement is not None and distance > 70:
                        print('Debug 144')
                        if itemName == 'boss':
                            self.fight.force_fight = False
                        if self.paused is True:
                            return False
                        self.send_text_to_bot.send('DEBUG: ' + itemName + ' too far (' + str(
                            (tmp_timeout - timeout) * -1) + '/' + str(timeout) + ')', self.from_python, "red")
                        tmp_timeout -= 1
                        time.sleep(1)
                else:
                    if itemName == 'boss':
                        self.fight.force_fight = False
                    if self.paused is True:
                        return False
                    if itemName == 'blacksmith' or itemName == 'exit_portal':
                        if feedback_image is not None:
                            print('Debug 333')
                            time.sleep(1)
                            feedback_image_coords = self.moveplayer.founfIconInScreen(
                                self.img_path + path, feedback_image, 1, False, self.captureWorker.screenshot, False, False, 0.8)
                            if feedback_image_coords == (0, 0):
                                print('Debug 444')
                                self.moveplayer.processing_movement_output(
                                        movementsBoss[random.randint(0, 7)])
                                time.sleep(1)
                                self.moveplayer.processing_movement_output('NK')
                    self.send_text_to_bot.send('DEBUG: not found ' + itemName + '(' + str(
                        (tmp_timeout - timeout) * -1) + '/' + str(timeout) + ')', self.from_python, "red")
                    tmp_timeout -= 1
                    time.sleep(1)

            if not foundedItem:
                print(
                    f'Debug: Item {itemName} not found within the specified timeout')
                print('Debug 15')
                print('DEBUG151: execute_action action_if_timeout',
                      action_if_timeout)
                if action_if_timeout is not None:
                    self.execute_action_if_timeout(action_if_timeout)
                    return False

            # Wait to disappear
            if wait_to_disappear:
                print('Debug 20')
                tmp_timeout = time_to_wait_to_disappear
                while tmp_timeout > 0:
                    if self.paused is True:
                        return False
                    print('Debug 21')
                    movement, distance = findSpecificItemOnMinimap(
                        self.captureWorker.screenshot, itemName, 1, True)
                    if movement is None and distance is None:
                        print('Debug 22')
                        break
                    time.sleep(1)
                    tmp_timeout -= 1
                if tmp_timeout <= 0:
                    print('Debug 23')
                    return False

                if time_to_wait_to_disappear is not None:
                    print('Debug 24')
                    for i in range(time_to_wait_to_disappear):
                        print('Debug 25')
                        if self.paused:
                            return False
                        self.send_text_to_bot.send(
                            str(time_to_wait_to_disappear - i) + f' sec left to wait {itemName} disappear.', self.from_python, 'purple')
                        time.sleep(1)

        return True

    def execute_action_if_timeout(self, action_if_timeout):
        for action in action_if_timeout:
            if action['action'] == 'go_to_step':
                self.return_to_old_step = True
                self.actual_step = action['step_num']
                # set executed false to this steps and all after
                for step in self.scenario[self.dungeon_name]['steps']:
                    if self.solo is True:
                        step['solo']['executed'] = False
                    else:
                        step['party']['executed'] = False

                    # print in purple
                    print("\033[95m" + str(self.scenario[self.dungeon_name]
                          ['steps'][self.actual_step]['name']) + "\033[0m")
                    print("\033[95m" + str(action['step_part']) + "\033[0m")
                    print("\033[95m" + str(action['feedback']) + "\033[0m")

                    self.actual_step = action['step_num']
                    # print in purple
                    print("\033[95m" + str(action['step_part']) + "\033[0m")
                    # print in pink
                    print("\033[95m" + str(self.scenario[self.dungeon_name]
                          ['steps'][self.actual_step]['solo']) + "\033[0m")
                    # print in orange
                    print("\033[95m" + str(self.scenario[self.dungeon_name]
                                           ['steps'][self.actual_step]['name']) + "\033[0m")
                    # print in purple
                    print("\033[95m" + str(action['feedback']) + "\033[0m")
                if self.solo is True:
                    self.execute_step(action['step_part'], self.scenario[self.dungeon_name]['steps'][self.actual_step]
                                      ['solo'], self.scenario[self.dungeon_name]['steps'][self.actual_step]['name'], action['feedback'])
                else:
                    self.execute_step(action['step_part'], self.scenario[self.dungeon_name]['steps'][self.actual_step]
                                      ['party'], self.scenario[self.dungeon_name]['steps'][self.actual_step]['name'], action['feedback'])
            else:
                self.execute_action_father(action)

    def execute_threads(self, threads):
        list_of_threads = []
        for thread in threads:
            for key in thread:
                if thread[key] is True:
                    # name purple
                    list_of_threads.append(
                        {'name': "\033[95m" + key + "\033[0m", 'action': "\033[92m" + 'resume' + "\033[0m"})
                    self.threads.resume_thread(key)
                else:
                    list_of_threads.append(
                        {'name': "\033[95m" + key + "\033[0m", 'action': "\033[91m" + 'pause' + "\033[0m"})
                    self.threads.pause_thread(key)

        if len(list_of_threads) > 0:
            if self.actual_threads_status is None:
                self.actual_threads_status = list_of_threads
            # compare actual status with new status and print only the changes
            for thread in list_of_threads:
                if thread not in self.actual_threads_status:
                    print(f"{thread['name']}--> {thread['action']}")
            self.actual_threads_status = list_of_threads

    def execute_this_step(self, step):
        if self.player_is_dead is True and step is False and step is True:
            return False
        else:
            return True

    def process_feedback(self, feedback, check_recorded_movements=False):
        feedback_after_coords = self.moveplayer.founfIconInScreen(
            self.img_path + feedback['path'], feedback['file'], 0, False, self.captureWorker.screenshot, False)
        if feedback['need_found'] is True:
            while feedback_after_coords == (0, 0):
                if check_recorded_movements is True:
                    if self.execute_last_movement() is False:
                        return False
                feedback_after_coords = self.moveplayer.founfIconInScreen(
                    self.img_path + feedback['path'], feedback['file'], 0, False, self.captureWorker.screenshot, False)
                time.sleep(0.5)
        if feedback['need_found'] is False:
            while feedback_after_coords != (0, 0):
                if check_recorded_movements is True:
                    if self.execute_last_movement():
                        return False
                feedback_after_coords = self.moveplayer.founfIconInScreen(
                    self.img_path + feedback['path'], feedback['file'], 0, False, self.captureWorker.screenshot, False)
                time.sleep(0.5)
        self.moveplayer.processing_movement_output('NK')
        self.moveplayer.processing_movement_output('NK')
        self.moveplayer.processing_movement_output('NK')
        if 'threads' in feedback:
            for thread in feedback['threads']:
                for key in thread:
                    if thread[key] is True:
                        self.threads.resume_thread(key)
                    else:
                        self.threads.pause_thread(key)
        if feedback['action'] == 'click':
            if feedback['coords'] != (1, 1):
                self.moveplayer.clickOnCoords(feedback['coords'])
            else:
                self.moveplayer.clickOnCoords(feedback_after_coords)

    def execute_last_movement(self):
        if self.dungeonWorker.record_movements is True:
            self.threads.pause_thread('DungeonWorker')
            last_movements = self.dungeonWorker.recorded_movements
            if len(last_movements) > 0:
                # get the last movement, execute it and remove it from recorded_movements
                last_movement = last_movements.pop()
                self.send_text_to_bot.send(
                    'Executing reverse last movement' + last_movement, self.from_python)
                print('Executing reverse last movement' + last_movement)
                self.moveplayer.processing_reverse_movement_output(
                    last_movement)
                time.sleep(0.3)
                self.moveplayer.processing_reverse_movement_output('NK')
                self.dungeonWorker.recorded_movements = last_movements
                return True
            else:
                return False

    def position_of_players(self, position):
        if position == 1:
            return (129, 63)
        elif position == 2:
            return (197, 67)
        elif position == 3:
            return (254, 66)
        else:
            return (129, 63)

    def follow_player(self):
        self.threads.pause_thread('Fight')
        self.threads.pause_thread('DungeonWorker')
        self.moveplayer.processing_movement_output('NK')
        time.sleep(1)
        self.moveplayer.clickOnCoords(
            self.position_of_players(self.follow_player_number))
        time.sleep(1)
        player_coords = self.moveplayer.founfIconInScreen(
            self.img_path + '\\game_items', 'follow_' + self.language, 1, False, self.captureWorker.screenshot)
        if player_coords != (0, 0):
            self.moveplayer.clickOnCoords(player_coords)
            self.moveplayer.clickOnCoords(
                self.position_of_players(self.follow_player_number))
            self.following_player = True
            return True
        else:
            return False

    def setAllStepsToFalse(self):
        self.fight.force_fight = False
        self.actual_step = 0
        self.threads.pause_thread('CheckDungeonTime')
        self.CheckDungeonTime.actual_time = 0
        if not hasattr(self.CheckDungeonTime, 'tmp_dungeon_over_time'):
            self.CheckDungeonTime.tmp_dungeon_over_time = self.CheckDungeonTime.dungeon_over_time
        else:
            if self.CheckDungeonTime.dungeon_over_time != self.CheckDungeonTime.tmp_dungeon_over_time:
                self.CheckDungeonTime.dungeon_over_time = self.CheckDungeonTime.tmp_dungeon_over_time
        self.checkpoint_after_die = None
        self.CheckDungeonMandatoryStep.dungeon_images = None
        for step in self.scenario[self.dungeon_name]['steps']:
            if self.solo is False:
                if 'party' in step and step['party'] is not None and 'before_start' in step['party'] and step['party']['before_start'] is not None and 'executed' in step['party']['before_start']:
                    step['party']['before_start']['executed'] = False

                if 'party' in step and step['party'] is not None and 'in_progress' in step['party'] and step['party']['in_progress'] is not None and 'executed' in step['party']['in_progress']:
                    step['party']['in_progress']['executed'] = False

                if 'party' in step and step['party'] is not None and 'after_end' in step['party'] and step['party']['after_end'] is not None and 'executed' in step['party']['after_end']:
                    step['party']['after_end']['executed'] = False

            else:
                if 'solo' in step and step['solo'] is not None and 'before_start' in step['solo'] and step['solo']['before_start'] is not None and 'executed' in step['solo']['before_start']:
                    step['solo']['before_start']['executed'] = False
                if 'solo' in step and step['solo'] is not None and 'in_progress' in step['solo'] and step['solo']['in_progress'] is not None and 'executed' in step['solo']['in_progress']:
                    step['solo']['in_progress']['executed'] = False
                if 'solo' in step and step['solo'] is not None and 'after_end' in step['solo'] and step['solo']['after_end'] is not None and 'executed' in step['solo']['after_end']:
                    step['solo']['after_end']['executed'] = False

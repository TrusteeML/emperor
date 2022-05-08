var EmperorController = function () {
    var findMax = function (nums) {
        var index = 0;
        for (var i = 0; i < nums.length; i++) {
            index = nums[i] > nums[index] ? i : index;
        }
        return index;
    };

    this.predict = function (features) {
        var classes = new Array(6);

        if (features[0] <= 0.22674418985843658) {
            if (features[0] <= 0.12209302186965942) {
                if (features[1] <= 1.3991075158119202) {
                    if (features[9] <= 0.12537232786417007) {
                        if (features[1] <= 1.1629876494407654) {
                            classes[0] = 1498;
                            classes[1] = 10;
                            classes[2] = 0;
                            classes[3] = 0;
                            classes[4] = 0;
                            classes[5] = 0;
                        } else {
                            if (features[9] <= 0.08526449277997017) {
                                classes[0] = 499;
                                classes[1] = 27;
                                classes[2] = 0;
                                classes[3] = 0;
                                classes[4] = 0;
                                classes[5] = 0;
                            } else {
                                if (features[15] <= 0.14204403012990952) {
                                    classes[0] = 9;
                                    classes[1] = 43;
                                    classes[2] = 0;
                                    classes[3] = 0;
                                    classes[4] = 0;
                                    classes[5] = 0;
                                } else {
                                    classes[0] = 103;
                                    classes[1] = 58;
                                    classes[2] = 0;
                                    classes[3] = 0;
                                    classes[4] = 0;
                                    classes[5] = 0;
                                }
                            }
                        }
                    } else {
                        if (features[1] <= 1.0066574215888977) {
                            if (features[9] <= 0.1842331513762474) {
                                classes[0] = 123;
                                classes[1] = 8;
                                classes[2] = 0;
                                classes[3] = 0;
                                classes[4] = 0;
                                classes[5] = 0;
                            } else {
                                classes[0] = 10;
                                classes[1] = 42;
                                classes[2] = 0;
                                classes[3] = 0;
                                classes[4] = 0;
                                classes[5] = 0;
                            }
                        } else {
                            classes[0] = 30;
                            classes[1] = 142;
                            classes[2] = 0;
                            classes[3] = 1;
                            classes[4] = 0;
                            classes[5] = 0;
                        }
                    }
                } else {
                    if (features[9] <= 0.0717957504093647) {
                        if (features[1] <= 1.4966329336166382) {
                            classes[0] = 93;
                            classes[1] = 31;
                            classes[2] = 0;
                            classes[3] = 0;
                            classes[4] = 0;
                            classes[5] = 0;
                        } else {
                            classes[0] = 30;
                            classes[1] = 86;
                            classes[2] = 0;
                            classes[3] = 0;
                            classes[4] = 0;
                            classes[5] = 0;
                        }
                    } else {
                        classes[0] = 43;
                        classes[1] = 302;
                        classes[2] = 0;
                        classes[3] = 0;
                        classes[4] = 0;
                        classes[5] = 0;
                    }
                }
            } else {
                if (features[1] <= 1.058088481426239) {
                    if (features[17] <= 0.19886227697134018) {
                        classes[0] = 8;
                        classes[1] = 249;
                        classes[2] = 0;
                        classes[3] = 12;
                        classes[4] = 0;
                        classes[5] = 0;
                    } else {
                        if (features[8] <= 0.11239650100469589) {
                            if (features[1] <= 0.8756178617477417) {
                                classes[0] = 422;
                                classes[1] = 13;
                                classes[2] = 0;
                                classes[3] = 0;
                                classes[4] = 0;
                                classes[5] = 0;
                            } else {
                                if (features[9] <= 0.06762038171291351) {
                                    classes[0] = 119;
                                    classes[1] = 17;
                                    classes[2] = 0;
                                    classes[3] = 0;
                                    classes[4] = 0;
                                    classes[5] = 0;
                                } else {
                                    classes[0] = 41;
                                    classes[1] = 55;
                                    classes[2] = 0;
                                    classes[3] = 0;
                                    classes[4] = 0;
                                    classes[5] = 0;
                                }
                            }
                        } else {
                            classes[0] = 23;
                            classes[1] = 75;
                            classes[2] = 0;
                            classes[3] = 0;
                            classes[4] = 0;
                            classes[5] = 0;
                        }
                    }
                } else {
                    if (features[9] <= 0.19034461677074432) {
                        if (features[1] <= 2.191075086593628) {
                            if (features[9] <= 0.053612397983670235) {
                                if (features[1] <= 1.240967571735382) {
                                    classes[0] = 44;
                                    classes[1] = 19;
                                    classes[2] = 0;
                                    classes[3] = 0;
                                    classes[4] = 0;
                                    classes[5] = 0;
                                } else {
                                    classes[0] = 2;
                                    classes[1] = 82;
                                    classes[2] = 0;
                                    classes[3] = 0;
                                    classes[4] = 0;
                                    classes[5] = 0;
                                }
                            } else {
                                classes[0] = 69;
                                classes[1] = 5120;
                                classes[2] = 3;
                                classes[3] = 87;
                                classes[4] = 0;
                                classes[5] = 0;
                            }
                        } else {
                            if (features[9] <= 0.15409698337316513) {
                                classes[0] = 0;
                                classes[1] = 332;
                                classes[2] = 2;
                                classes[3] = 84;
                                classes[4] = 0;
                                classes[5] = 0;
                            } else {
                                classes[0] = 0;
                                classes[1] = 44;
                                classes[2] = 2;
                                classes[3] = 80;
                                classes[4] = 0;
                                classes[5] = 0;
                            }
                        }
                    } else {
                        if (features[1] <= 1.9556803107261658) {
                            if (features[9] <= 0.24868430197238922) {
                                classes[0] = 0;
                                classes[1] = 321;
                                classes[2] = 2;
                                classes[3] = 59;
                                classes[4] = 0;
                                classes[5] = 0;
                            } else {
                                classes[0] = 0;
                                classes[1] = 76;
                                classes[2] = 0;
                                classes[3] = 91;
                                classes[4] = 0;
                                classes[5] = 0;
                            }
                        } else {
                            classes[0] = 0;
                            classes[1] = 31;
                            classes[2] = 1;
                            classes[3] = 179;
                            classes[4] = 0;
                            classes[5] = 0;
                        }
                    }
                }
            }
        } else {
            if (features[0] <= 0.546511635184288) {
                if (features[9] <= 0.10852978378534317) {
                    if (features[17] <= 1.1575629711151123) {
                        if (features[1] <= 1.3956983089447021) {
                            classes[0] = 1;
                            classes[1] = 119;
                            classes[2] = 0;
                            classes[3] = 8;
                            classes[4] = 0;
                            classes[5] = 0;
                        } else {
                            classes[0] = 0;
                            classes[1] = 36;
                            classes[2] = 4;
                            classes[3] = 49;
                            classes[4] = 0;
                            classes[5] = 0;
                        }
                    } else {
                        if (features[1] <= 0.9067513942718506) {
                            classes[0] = 59;
                            classes[1] = 5;
                            classes[2] = 0;
                            classes[3] = 0;
                            classes[4] = 0;
                            classes[5] = 0;
                        } else {
                            classes[0] = 8;
                            classes[1] = 29;
                            classes[2] = 0;
                            classes[3] = 0;
                            classes[4] = 0;
                            classes[5] = 0;
                        }
                    }
                } else {
                    if (features[1] <= 1.0751867294311523) {
                        if (features[9] <= 0.18051490932703018) {
                            classes[0] = 0;
                            classes[1] = 83;
                            classes[2] = 1;
                            classes[3] = 22;
                            classes[4] = 0;
                            classes[5] = 0;
                        } else {
                            classes[0] = 0;
                            classes[1] = 6;
                            classes[2] = 0;
                            classes[3] = 64;
                            classes[4] = 0;
                            classes[5] = 0;
                        }
                    } else {
                        if (features[9] <= 0.13295313715934753) {
                            if (features[1] <= 1.3469969034194946) {
                                classes[0] = 0;
                                classes[1] = 35;
                                classes[2] = 0;
                                classes[3] = 30;
                                classes[4] = 0;
                                classes[5] = 0;
                            } else {
                                classes[0] = 0;
                                classes[1] = 22;
                                classes[2] = 5;
                                classes[3] = 203;
                                classes[4] = 0;
                                classes[5] = 0;
                            }
                        } else {
                            if (features[1] <= 3.1133062839508057) {
                                classes[0] = 0;
                                classes[1] = 22;
                                classes[2] = 14;
                                classes[3] = 3926;
                                classes[4] = 2;
                                classes[5] = 23;
                            } else {
                                classes[0] = 0;
                                classes[1] = 0;
                                classes[2] = 0;
                                classes[3] = 100;
                                classes[4] = 0;
                                classes[5] = 36;
                            }
                        }
                    }
                }
            } else {
                if (features[1] <= 1.321736216545105) {
                    classes[0] = 2;
                    classes[1] = 0;
                    classes[2] = 1;
                    classes[3] = 30;
                    classes[4] = 0;
                    classes[5] = 10;
                } else {
                    classes[0] = 0;
                    classes[1] = 0;
                    classes[2] = 0;
                    classes[3] = 17;
                    classes[4] = 0;
                    classes[5] = 526;
                }
            }
        }

        return findMax(classes);
    };
};

export default EmperorController;

var DecisionTreeClassifier = function() {

    var findMax = function(nums) {
        var index = 0;
        for (var i = 0; i < nums.length; i++) {
            index = nums[i] > nums[index] ? i : index;
        }
        return index;
    };

    this.predict = function(features) {
        var classes = new Array(6);
            
        if (features[1] <= 2.023919701576233) {
            if (features[1] <= 0.9844183027744293) {
                if (features[9] <= 0.16084956377744675) {
                    if (features[7] <= 0.11977006122469902) {
                        if (features[1] <= 0.8612149357795715) {
                            if (features[14] <= 2.889526128768921) {
                                if (features[8] <= 0.21221348643302917) {
                                    if (features[0] <= 0.302325576543808) {
                                        if (features[9] <= 0.13002048432826996) {
                                            classes[0] = 22258; 
                                            classes[1] = 0; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        } else {
                                            if (features[1] <= 0.7069400548934937) {
                                                if (features[6] <= 0.1141340471804142) {
                                                    if (features[24] <= 0.05208333395421505) {
                                                        if (features[14] <= 1.4761791825294495) {
                                                            classes[0] = 0; 
                                                            classes[1] = 0; 
                                                            classes[2] = 19; 
                                                            classes[3] = 0; 
                                                            classes[4] = 0; 
                                                            classes[5] = 0; 
                                                        } else {
                                                            classes[0] = 23; 
                                                            classes[1] = 0; 
                                                            classes[2] = 0; 
                                                            classes[3] = 0; 
                                                            classes[4] = 0; 
                                                            classes[5] = 0; 
                                                        }
                                                    } else {
                                                        if (features[5] <= 0.09966319426894188) {
                                                            classes[0] = 1783; 
                                                            classes[1] = 0; 
                                                            classes[2] = 0; 
                                                            classes[3] = 0; 
                                                            classes[4] = 0; 
                                                            classes[5] = 0; 
                                                        } else {
                                                            if (features[13] <= 0.40104956924915314) {
                                                                classes[0] = 125; 
                                                                classes[1] = 0; 
                                                                classes[2] = 0; 
                                                                classes[3] = 0; 
                                                                classes[4] = 0; 
                                                                classes[5] = 0; 
                                                            } else {
                                                                classes[0] = 0; 
                                                                classes[1] = 21; 
                                                                classes[2] = 0; 
                                                                classes[3] = 0; 
                                                                classes[4] = 0; 
                                                                classes[5] = 0; 
                                                            }
                                                        }
                                                    }
                                                } else {
                                                    if (features[7] <= 0.062174320220947266) {
                                                        classes[0] = 18; 
                                                        classes[1] = 0; 
                                                        classes[2] = 0; 
                                                        classes[3] = 0; 
                                                        classes[4] = 0; 
                                                        classes[5] = 0; 
                                                    } else {
                                                        classes[0] = 0; 
                                                        classes[1] = 21; 
                                                        classes[2] = 0; 
                                                        classes[3] = 0; 
                                                        classes[4] = 0; 
                                                        classes[5] = 0; 
                                                    }
                                                }
                                            } else {
                                                if (features[20] <= 0.5885870158672333) {
                                                    classes[0] = 0; 
                                                    classes[1] = 106; 
                                                    classes[2] = 0; 
                                                    classes[3] = 0; 
                                                    classes[4] = 0; 
                                                    classes[5] = 0; 
                                                } else {
                                                    if (features[6] <= 0.04410501383244991) {
                                                        classes[0] = 0; 
                                                        classes[1] = 32; 
                                                        classes[2] = 0; 
                                                        classes[3] = 0; 
                                                        classes[4] = 0; 
                                                        classes[5] = 0; 
                                                    } else {
                                                        classes[0] = 237; 
                                                        classes[1] = 0; 
                                                        classes[2] = 0; 
                                                        classes[3] = 0; 
                                                        classes[4] = 0; 
                                                        classes[5] = 0; 
                                                    }
                                                }
                                            }
                                        }
                                    } else {
                                        if (features[11] <= 0.3330647349357605) {
                                            classes[0] = 45; 
                                            classes[1] = 0; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        } else {
                                            classes[0] = 0; 
                                            classes[1] = 38; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        }
                                    }
                                } else {
                                    classes[0] = 0; 
                                    classes[1] = 18; 
                                    classes[2] = 0; 
                                    classes[3] = 0; 
                                    classes[4] = 0; 
                                    classes[5] = 0; 
                                }
                            } else {
                                if (features[13] <= 0.9411368668079376) {
                                } else {
                                }
                            }
                        } else {
                            if (features[4] <= 0.1130559965968132) {
                                if (features[2] <= 0.10813721269369125) {
                                    if (features[7] <= 0.11037269607186317) {
                                        classes[0] = 1559; 
                                        classes[1] = 0; 
                                        classes[2] = 0; 
                                        classes[3] = 0; 
                                        classes[4] = 0; 
                                        classes[5] = 0; 
                                    } else {
                                        if (features[20] <= 0.5886645019054413) {
                                            classes[0] = 0; 
                                            classes[1] = 27; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        } else {
                                            classes[0] = 71; 
                                            classes[1] = 0; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        }
                                    }
                                } else {
                                    if (features[18] <= 0.16289199888706207) {
                                        if (features[5] <= 0.11065559089183807) {
                                            classes[0] = 205; 
                                            classes[1] = 0; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        } else {
                                            classes[0] = 0; 
                                            classes[1] = 38; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        }
                                    } else {
                                        if (features[11] <= 0.3191074877977371) {
                                            classes[0] = 17; 
                                            classes[1] = 0; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        } else {
                                            classes[0] = 0; 
                                            classes[1] = 79; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        }
                                    }
                                }
                            } else {
                                if (features[19] <= 0.38641148805618286) {
                                    if (features[7] <= 0.07730845361948013) {
                                        classes[0] = 61; 
                                        classes[1] = 0; 
                                        classes[2] = 0; 
                                        classes[3] = 0; 
                                        classes[4] = 0; 
                                        classes[5] = 0; 
                                    } else {
                                        if (features[10] <= 0.23904486745595932) {
                                            classes[0] = 30; 
                                            classes[1] = 0; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        } else {
                                            classes[0] = 0; 
                                            classes[1] = 251; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        }
                                    }
                                } else {
                                    if (features[7] <= 0.10880152508616447) {
                                        classes[0] = 216; 
                                        classes[1] = 0; 
                                        classes[2] = 0; 
                                        classes[3] = 0; 
                                        classes[4] = 0; 
                                        classes[5] = 0; 
                                    } else {
                                        classes[0] = 0; 
                                        classes[1] = 20; 
                                        classes[2] = 0; 
                                        classes[3] = 0; 
                                        classes[4] = 0; 
                                        classes[5] = 0; 
                                    }
                                }
                            }
                        }
                    } else {
                        if (features[1] <= 0.7742400169372559) {
                            if (features[9] <= 0.1416480764746666) {
                                if (features[15] <= 0.33341558277606964) {
                                } else {
                                }
                            } else {
                                if (features[8] <= 0.1336558684706688) {
                                    classes[0] = 48; 
                                    classes[1] = 0; 
                                    classes[2] = 0; 
                                    classes[3] = 0; 
                                    classes[4] = 0; 
                                    classes[5] = 0; 
                                } else {
                                    classes[0] = 0; 
                                    classes[1] = 134; 
                                    classes[2] = 0; 
                                    classes[3] = 0; 
                                    classes[4] = 0; 
                                    classes[5] = 0; 
                                }
                            }
                        } else {
                            if (features[5] <= 0.09068094193935394) {
                            } else {
                            }
                        }
                    }
                } else {
                    if (features[8] <= 0.1342402920126915) {
                        if (features[9] <= 0.24861252307891846) {
                        } else {
                        }
                    } else {
                        if (features[0] <= 0.302325576543808) {
                            if (features[11] <= 1.2860673666000366) {
                                if (features[9] <= 0.17605481296777725) {
                                } else {
                                }
                            } else {
                                classes[0] = 0; 
                                classes[1] = 0; 
                                classes[2] = 0; 
                                classes[3] = 39; 
                                classes[4] = 0; 
                                classes[5] = 0; 
                            }
                        } else {
                            if (features[1] <= 0.5808188915252686) {
                                if (features[11] <= 0.36477240920066833) {
                                } else {
                                }
                            } else {
                                if (features[8] <= 0.2717510312795639) {
                                    if (features[3] <= 0.1983548104763031) {
                                        classes[0] = 0; 
                                        classes[1] = 101; 
                                        classes[2] = 0; 
                                        classes[3] = 0; 
                                        classes[4] = 0; 
                                        classes[5] = 0; 
                                    } else {
                                        if (features[1] <= 0.900247186422348) {
                                            if (features[8] <= 0.25946474075317383) {
                                            } else {
                                            }
                                        } else {
                                            classes[0] = 0; 
                                            classes[1] = 24; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        }
                                    }
                                } else {
                                    classes[0] = 0; 
                                    classes[1] = 0; 
                                    classes[2] = 0; 
                                    classes[3] = 341; 
                                    classes[4] = 0; 
                                    classes[5] = 0; 
                                }
                            }
                        }
                    }
                }
            } else {
                if (features[0] <= 0.35465116798877716) {
                    if (features[0] <= 0.12209302186965942) {
                    } else {
                    }
                } else {
                    if (features[17] <= 0.8958404660224915) {
                        if (features[0] <= 0.7151162773370743) {
                            if (features[1] <= 1.269054114818573) {
                                if (features[9] <= 0.14473383873701096) {
                                    if (features[15] <= 0.4061923623085022) {
                                        classes[0] = 0; 
                                        classes[1] = 0; 
                                        classes[2] = 0; 
                                        classes[3] = 40; 
                                        classes[4] = 0; 
                                        classes[5] = 0; 
                                    } else {
                                        if (features[15] <= 0.7764077484607697) {
                                            classes[0] = 0; 
                                            classes[1] = 155; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        } else {
                                            classes[0] = 0; 
                                            classes[1] = 0; 
                                            classes[2] = 0; 
                                            classes[3] = 15; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        }
                                    }
                                } else {
                                    if (features[1] <= 1.0232890844345093) {
                                        if (features[17] <= 0.44293901324272156) {
                                        } else {
                                        }
                                    } else {
                                        if (features[12] <= 1.115980178117752) {
                                            if (features[19] <= 0.4357855021953583) {
                                            } else {
                                            }
                                        } else {
                                            classes[0] = 0; 
                                            classes[1] = 32; 
                                            classes[2] = 0; 
                                            classes[3] = 0; 
                                            classes[4] = 0; 
                                            classes[5] = 0; 
                                        }
                                    }
                                }
                            } else {
                                if (features[14] <= 0.08041620627045631) {
                                    classes[0] = 0; 
                                    classes[1] = 16; 
                                    classes[2] = 0; 
                                    classes[3] = 0; 
                                    classes[4] = 0; 
                                    classes[5] = 0; 
                                } else {
                                    if (features[8] <= 0.10072188451886177) {
                                    } else {
                                    }
                                }
                            }
                        } else {
                            if (features[4] <= 0.43389202654361725) {
                                if (features[1] <= 1.1847805976867676) {
                                    classes[0] = 0; 
                                    classes[1] = 0; 
                                    classes[2] = 0; 
                                    classes[3] = 34; 
                                    classes[4] = 0; 
                                    classes[5] = 0; 
                                } else {
                                    if (features[12] <= 0.6008960008621216) {
                                    } else {
                                    }
                                }
                            } else {
                                if (features[23] <= 2.049772024154663) {
                                    classes[0] = 0; 
                                    classes[1] = 0; 
                                    classes[2] = 0; 
                                    classes[3] = 0; 
                                    classes[4] = 0; 
                                    classes[5] = 16; 
                                } else {
                                    classes[0] = 0; 
                                    classes[1] = 0; 
                                    classes[2] = 0; 
                                    classes[3] = 87; 
                                    classes[4] = 0; 
                                    classes[5] = 0; 
                                }
                            }
                        }
                    } else {
                        if (features[1] <= 1.6287946701049805) {
                            if (features[9] <= 0.07043907046318054) {
                                classes[0] = 54; 
                                classes[1] = 0; 
                                classes[2] = 0; 
                                classes[3] = 0; 
                                classes[4] = 0; 
                                classes[5] = 0; 
                            } else {
                                classes[0] = 0; 
                                classes[1] = 327; 
                                classes[2] = 0; 
                                classes[3] = 0; 
                                classes[4] = 0; 
                                classes[5] = 0; 
                            }
                        } else {
                            classes[0] = 0; 
                            classes[1] = 0; 
                            classes[2] = 0; 
                            classes[3] = 105; 
                            classes[4] = 0; 
                            classes[5] = 0; 
                        }
                    }
                }
            }
        } else {
            if (features[9] <= 0.3779938817024231) {
            } else {
            }
        }
    
        return findMax(classes);
    };

};

if (typeof process !== 'undefined' && typeof process.argv !== 'undefined') {
    if (process.argv.length - 2 === 25) {

        // Features:
        var features = process.argv.slice(2);

        // Prediction:
        var clf = new DecisionTreeClassifier();
        var prediction = clf.predict(features);
        console.log(prediction);

    }
}
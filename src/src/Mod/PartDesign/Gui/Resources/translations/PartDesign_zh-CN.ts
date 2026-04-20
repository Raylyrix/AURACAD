<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="zh-CN" sourcelanguage="en">
  <context>
    <name>App::Property</name>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="82"/>
      <source>The center point of the helix' start; derived from the reference axis.</source>
      <translation>èžºæ—‹çº¿å¼€å§‹çš„ä¸­å¿ƒç‚¹; æºè‡ªå‚è€ƒè½´ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="92"/>
      <source>The helix' direction; derived from the reference axis.</source>
      <translation>èžºæ—‹æ–¹å‘ï¼›æ´¾ç”Ÿè‡ªå‚è€ƒè½´ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="99"/>
      <source>The reference axis of the helix.</source>
      <translation>èžºæ—‹å‚è€ƒè½´ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="106"/>
      <source>The helix input mode specifies which properties are set by the user.
Dependent properties are then calculated.</source>
      <translation>èžºæ—‹çº¿è¾“å…¥æ¨¡å¼æŒ‡å®šäº†é‚£äº›éœ€è¦ç”¨æˆ·è®¾ç½®çš„å±žæ€§ã€‚
ç„¶åŽè®¡ç®—ä¾èµ–çš„å±žæ€§ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="118"/>
      <source>The axial distance between two turns.</source>
      <translation>ä¸¤åœˆä¹‹é—´çš„å‚è€ƒè½´æ–¹å‘çš„è·ç¦»ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="125"/>
      <source>The height of the helix' path, not accounting for the extent of the profile.</source>
      <translation>èžºæ—‹çº¿è·¯å¾„çš„é«˜åº¦ï¼Œä¸è®¡å…¥å‰–é¢çš„å¤§å°ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="135"/>
      <source>The number of turns in the helix.</source>
      <translation>èžºæ—‹çº¿çš„åœˆæ•°</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="143"/>
      <source>The angle of the cone that forms a hull around the helix.
Non-zero values turn the helix into a conical spiral.
Positive values make the radius grow, negative shrinks.</source>
      <translation>å›´ç»•èžºæ—‹çº¿å½¢æˆåŒ…ç»œé¢çš„åœ†é”¥è§’åº¦ã€‚
éžé›¶å€¼ä¼šå°†èžºæ—‹çº¿è½¬æ¢ä¸ºé”¥çŠ¶èžºæ—‹ã€‚
æ­£å€¼ä½¿åŠå¾„å¢žå¤§ï¼Œè´Ÿå€¼ä½¿åŠå¾„ç¼©å°ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="156"/>
      <source>The growth of the helix' radius per turn.
Non-zero values turn the helix into a conical spiral.</source>
      <translation>èžºæ—‹çº¿æ¯åœˆçš„åŠå¾„çš„å¢žé•¿ã€‚
éžé›¶å€¼å°†èžºæ—‹çº¿å˜æˆé”¥å½¢èžºæ—‹ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="167"/>
      <source>Sets the turning direction to left handed,
i.e. counter-clockwise when moving along its axis.</source>
      <translation>å°†è½¬å‘æ–¹å‘è®¾ç½®ä¸ºå·¦è¡Œï¼Œ
å³æ²¿å…¶è½´ç§»åŠ¨æ—¶é€†æ—¶é’ˆã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="178"/>
      <source>Determines whether the helix points in the opposite direction of the axis.</source>
      <translation>ç¡®å®šèžºæ—‹ç‚¹æ˜¯å¦ä½äºŽè½´çš„ç›¸åæ–¹å‘ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="188"/>
      <source>If set, the result will be the intersection of the profile and the preexisting body.</source>
      <translation>å¦‚æžœè®¾ç½®ï¼Œå¦‚æžœè®¾å®šï¼Œç»“æžœå°†æ˜¯è½®å»“ä¸Žå…ˆå­˜ä½“çš„äº¤é›†ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="198"/>
      <source>If false, the tool will propose an initial value for the pitch based on the profile bounding box,
so that self intersection is avoided.</source>
      <translation>å¦‚æžœæ˜¯å‡çš„ï¼Œè¯¥å·¥å…·å°†åŸºäºŽè½®å»“è¾¹ç•Œæ¡†ä¸ºèžºè·æå‡ºåˆå§‹å€¼ï¼Œï¼Œä»Žè€Œé¿å…è‡ªç›¸äº¤ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="210"/>
      <source>Fusion Tolerance for the Helix, increase if helical shape does not merge nicely with part.</source>
      <translation>èžºæ—‹çš„ç»“åˆå…¬å·®ï¼Œå¦‚æžœèžºæ—‹å½¢çŠ¶ä¸èƒ½ä¸Žé›¶ä»¶å¾ˆå¥½åœ°ç»“åˆï¼Œåˆ™å¢žåŠ ã€‚</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.py" line="108"/>
      <source>Number of gear teeth</source>
      <translation>é½¿æ•°</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.py" line="120"/>
      <source>Pressure angle of gear teeth</source>
      <translation>åŽ‹åŠ›è§’</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.py" line="114"/>
      <source>Module of the gear</source>
      <translation>é½¿è½®æ¨¡æ•°</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.py" line="129"/>
      <source>True=2 curves with each 3 control points, False=1 curve with 4 control points.</source>
      <translation>True=2 æ›²çº¿æœ‰3ä¸ªæŽ§åˆ¶ç‚¹ï¼ŒFalse=1 æ›²çº¿æœ‰4ä¸ªæŽ§åˆ¶ç‚¹ã€‚</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.py" line="137"/>
      <source>True=external Gear, False=internal Gear</source>
      <translation>True=å¤–é½¿è½®ï¼ŒFalse=å†…é½¿è½®</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.py" line="146"/>
      <source>The height of the tooth from the pitch circle up to its tip, normalized by the module.</source>
      <translation>ä»ŽèŠ‚åœ†åˆ°é½¿é¡¶çš„é«˜åº¦ï¼Œä»¥æ¨¡æ•°å½’ä¸€åŒ–ã€‚</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.py" line="155"/>
      <source>The height of the tooth from the pitch circle down to its root, normalized by the module.</source>
      <translation>ä»ŽèŠ‚åœ†åˆ°é½¿æ ¹çš„é«˜åº¦ï¼Œä»¥æ¨¡æ•°å½’ä¸€åŒ–ã€‚</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.py" line="164"/>
      <source>The radius of the fillet at the root of the tooth, normalized by the module.</source>
      <translation>é½¿æ ¹åœ†è§’åŠå¾„ï¼Œä»¥æ¨¡æ•°å½’ä¸€åŒ–ã€‚</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.py" line="173"/>
      <source>The distance by which the reference profile is shifted outwards, normalized by the module.</source>
      <translation>å‚è€ƒè½®å»“å‘å¤–åç§»çš„è·ç¦»ï¼Œä»¥æ¨¡æ•°å½’ä¸€åŒ–ã€‚</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignAdditiveHelix</name>
    <message>
      <location filename="../../Command.cpp" line="1664"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1665"/>
      <source>Additive Helix</source>
      <translation>æ·»åŠ å¼èžºæ—‹</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1666"/>
      <source>Sweeps the selected sketch or profile along a helix and adds it to the body</source>
      <translation>æ²¿ç€èžºæ—‹çº¿æ‰«æé€‰å®šçš„è‰å›¾æˆ–è½®å»“ï¼Œå¹¶å°†å…¶æ·»åŠ åˆ°å®žä½“ä¸­</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignAdditiveLoft</name>
    <message>
      <location filename="../../Command.cpp" line="1565"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1566"/>
      <source>Additive Loft</source>
      <translation>æ·»åŠ å¼æ”¾æ ·</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1567"/>
      <source>Lofts the selected sketch or profile along a path and adds it to the body</source>
      <translation>æ²¿ç€è·¯å¾„æ”¾æ ·é€‰å®šçš„è‰å›¾æˆ–è½®å»“ï¼Œå¹¶å°†å…¶æ·»åŠ åˆ°å®žä½“ä¸­</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignAdditivePipe</name>
    <message>
      <location filename="../../Command.cpp" line="1465"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1466"/>
      <source>Additive Pipe</source>
      <translation>æ·»åŠ å¼ç®¡é“</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1467"/>
      <source>Sweeps the selected sketch or profile along a path and adds it to the body</source>
      <translation>æ²¿ç€è·¯å¾„æ‰«æé€‰å®šçš„è‰å›¾æˆ–è½®å»“ï¼Œå¹¶å°†å…¶æ·»åŠ åˆ°å®žä½“ä¸­</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignBody</name>
    <message>
      <location filename="../../CommandBody.cpp" line="92"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="93"/>
      <source>New Body</source>
      <translation>æ–°å»ºå®žä½“</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="94"/>
      <source>Creates a new body and activates it</source>
      <translation>åˆ›å»ºä¸€ä¸ªæ–°å®žä½“å¹¶æ¿€æ´»å®ƒ</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignBoolean</name>
    <message>
      <location filename="../../Command.cpp" line="2580"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2581"/>
      <source>Boolean Operation</source>
      <translation>å¸ƒå°”è¿ç®—</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2582"/>
      <source>Applies boolean operations with the selected objects and the active body</source>
      <translation>å¯¹é€‰å®šçš„å¯¹è±¡å’Œæ¿€æ´»çš„å®žä½“åº”ç”¨å¸ƒå°”è¿ç®—</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignCS</name>
    <message>
      <location filename="../../Command.cpp" line="282"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="283"/>
      <source>Local Coordinate System</source>
      <translation>å±€éƒ¨åæ ‡ç³»</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="284"/>
      <source>Creates a new local coordinate system</source>
      <translation>åˆ›å»ºä¸€ä¸ªæ–°çš„å±€éƒ¨åæ ‡ç³»</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignChamfer</name>
    <message>
      <location filename="../../Command.cpp" line="1991"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1992"/>
      <source>Chamfer</source>
      <translation>å€’è§’</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1993"/>
      <source>Applies a chamfer to the selected edges or faces</source>
      <translation>å¯¹é€‰å®šçš„è¾¹æˆ–é¢åº”ç”¨å€’è§’</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignClone</name>
    <message>
      <location filename="../../Command.cpp" line="492"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="493"/>
      <source>Clone</source>
      <translation>å…‹éš†</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="494"/>
      <source>Copies a solid object parametrically as the base feature of a new body</source>
      <translation>å°†ä¸€ä¸ªå®žä½“å¯¹è±¡å‚æ•°åŒ–åœ°å¤åˆ¶ä¸ºä¸€ä¸ªæ–°å®žä½“çš„åŸºæœ¬ç‰¹å¾</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignDraft</name>
    <message>
      <location filename="../../Command.cpp" line="2020"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2021"/>
      <source>Draft</source>
      <translation>æ‹”æ¨¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2022"/>
      <source>Applies a draft to the selected faces</source>
      <translation>å¯¹é€‰å®šçš„é¢åº”ç”¨æ‹”æ¨¡</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignDuplicateSelection</name>
    <message>
      <location filename="../../CommandBody.cpp" line="762"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="763"/>
      <source>Duplicate &amp;Object</source>
      <translation>å¤åˆ¶å¯¹è±¡(&amp;O)</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="764"/>
      <source>Duplicates the selected object and adds it to the active body</source>
      <translation>å¤åˆ¶æ‰€é€‰å¯¹è±¡å¹¶å°†å…¶æ·»åŠ åˆ°æ´»åŠ¨å®žä½“</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignFillet</name>
    <message>
      <location filename="../../Command.cpp" line="1963"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1964"/>
      <source>Fillet</source>
      <translation>åœ†è§’</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1965"/>
      <source>Applies a fillet to the selected edges or faces</source>
      <translation>å¯¹é€‰å®šçš„è¾¹æˆ–é¢åº”ç”¨åœ†è§’</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignGroove</name>
    <message>
      <location filename="../../Command.cpp" line="1395"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1396"/>
      <source>Groove</source>
      <translation>æŒ–æ§½</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1397"/>
      <source>Revolves the sketch or profile around a line or axis and removes it from the body</source>
      <translation>å›´ç»•ä¸€æ¡çº¿æˆ–ä¸€ä¸ªè½´çº¿æ—‹è½¬é€‰å®šçš„è‰å›¾æˆ–è½®å»“ï¼Œå¹¶å°†å…¶ä»Žå®žä½“ä¸­ç§»é™¤</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignHole</name>
    <message>
      <location filename="../../Command.cpp" line="1288"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1289"/>
      <source>Hole</source>
      <translation>å­”</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1291"/>
      <source>Creates holes in the active body at the center points of circles or arcs of the selected sketch or profile</source>
      <translation>åœ¨é€‰å®šè‰å›¾æˆ–è½®å»“ä¸­åœ†æˆ–åœ†å¼§çš„ä¸­å¿ƒç‚¹å¤„ï¼Œåœ¨æ¿€æ´»çš„å®žä½“ä¸Šåˆ›å»ºå­”</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignLine</name>
    <message>
      <location filename="../../Command.cpp" line="222"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="223"/>
      <source>Datum Line</source>
      <translation>åŸºå‡†çº¿</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="224"/>
      <source>Creates a new datum line</source>
      <translation>åˆ›å»ºä¸€ä¸ªæ–°çš„åŸºå‡†çº¿</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignLinearPattern</name>
    <message>
      <location filename="../../Command.cpp" line="2275"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2276"/>
      <source>Linear Pattern</source>
      <translation>çº¿æ€§é˜µåˆ—</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2277"/>
      <source>Duplicates the selected features or the active body in a linear pattern</source>
      <translation>ä»¥çº¿æ€§é˜µåˆ—çš„æ–¹å¼ï¼Œå¤åˆ¶é€‰å®šçš„ç‰¹å¾æˆ–æ¿€æ´»çš„å®žä½“</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignMigrate</name>
    <message>
      <location filename="../../CommandBody.cpp" line="392"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="393"/>
      <source>Migrate</source>
      <translation>è¿ç§»</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="394"/>
      <source>Migrates the document to the modern Part Design workflow</source>
      <translation>å°†æ–‡æ¡£è¿ç§»åˆ°çŽ°ä»£é›¶ä»¶è®¾è®¡å·¥ä½œæµ</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignMirrored</name>
    <message>
      <location filename="../../Command.cpp" line="2218"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2219"/>
      <source>Mirror</source>
      <translation>é•œåƒ</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2220"/>
      <source>Mirrors the selected features or active body</source>
      <translation>é•œåƒé€‰å®šçš„ç‰¹å¾æˆ–æ¿€æ´»çš„å®žä½“</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignMoveFeature</name>
    <message>
      <location filename="../../CommandBody.cpp" line="830"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="831"/>
      <source>Move Object Toâ€¦</source>
      <translation>ç§»åŠ¨å¯¹è±¡åˆ°â€¦</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="832"/>
      <source>Moves the selected object to another body</source>
      <translation>ç§»åŠ¨é€‰å®šå¯¹è±¡åˆ°å¦ä¸€ä¸ªå®žä½“</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignMoveFeatureInTree</name>
    <message>
      <location filename="../../CommandBody.cpp" line="1027"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1028"/>
      <source>Move Feature Afterâ€¦</source>
      <translation>å‘åŽç§»åŠ¨ç‰¹å¾â€¦</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1029"/>
      <source>Moves the selected feature after another feature in the same body</source>
      <translation>ç§»åŠ¨é€‰ä¸­çš„ç‰¹å¾åˆ°å¤„äºŽåŒä¸€å®žä½“çš„å…¶å®ƒç‰¹å¾åŽ</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignMoveTip</name>
    <message>
      <location filename="../../CommandBody.cpp" line="663"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="664"/>
      <source>Set Tip</source>
      <translation>è®¾ç½® Tip</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="665"/>
      <source>Moves the tip of the body to the selected feature</source>
      <translation>ç§»åŠ¨å®žä½“çš„æ ‡è¯†åˆ°é€‰å®šç‰¹å¾</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignMultiTransform</name>
    <message>
      <location filename="../../Command.cpp" line="2449"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2450"/>
      <source>Multi-Transform</source>
      <translation>å¤šå˜å½¢</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2451"/>
      <source>Applies multiple transformations to the selected features or active body</source>
      <translation>å°†å¤šä¸ªè½¬æ¢åº”ç”¨åˆ°é€‰å®šçš„ç‰¹å¾æˆ–æ´»åŠ¨å®žä½“</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignNewSketch</name>
    <message>
      <location filename="../../Command.cpp" line="577"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="578"/>
      <source>New Sketch</source>
      <translation>æ–°å»ºè‰å›¾</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="579"/>
      <source>Creates a new sketch</source>
      <translation>åˆ›å»ºä¸€ä¸ªæ–°çš„è‰å›¾</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignPad</name>
    <message>
      <location filename="../../Command.cpp" line="1230"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1231"/>
      <source>Pad</source>
      <translation>å‡¸å°</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1232"/>
      <source>Extrudes the selected sketch or profile and adds it to the body</source>
      <translation>æ‹‰ä¼¸é€‰å®šçš„è‰å›¾æˆ–è½®å»“å¹¶å°†å…¶æ·»åŠ åˆ°å®žä½“ä¸­</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignPlane</name>
    <message>
      <location filename="../../Command.cpp" line="192"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="193"/>
      <source>Datum Plane</source>
      <translation>åŸºå‡†é¢</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="194"/>
      <source>Creates a new datum plane</source>
      <translation>åˆ›å»ºä¸€ä¸ªæ–°çš„åŸºå‡†é¢</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignPocket</name>
    <message>
      <location filename="../../Command.cpp" line="1259"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1260"/>
      <source>Pocket</source>
      <translation>å‡¹å‘</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1261"/>
      <source>Extrudes the selected sketch or profile and removes it from the body</source>
      <translation>æ‹‰ä¼¸é€‰å®šçš„è‰å›¾æˆ–è½®å»“å¹¶å°†å…¶ä»Žå®žä½“ä¸­ç§»é™¤</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignPoint</name>
    <message>
      <location filename="../../Command.cpp" line="252"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="253"/>
      <source>Datum Point</source>
      <translation>åŸºå‡†ç‚¹</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="254"/>
      <source>Creates a new datum point</source>
      <translation>åˆ›å»ºä¸€ä¸ªæ–°çš„åŸºå‡†ç‚¹</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignPolarPattern</name>
    <message>
      <location filename="../../Command.cpp" line="2344"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2345"/>
      <source>Polar Pattern</source>
      <translation>çŽ¯å½¢é˜µåˆ—</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2346"/>
      <source>Duplicates the selected features or the active body in a circular pattern</source>
      <translation>ä»¥çŽ¯å½¢é˜µåˆ—çš„æ–¹å¼ï¼Œå¤åˆ¶é€‰å®šçš„ç‰¹å¾æˆ–æ¿€æ´»çš„å®žä½“</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignRevolution</name>
    <message>
      <location filename="../../Command.cpp" line="1333"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1334"/>
      <source>Revolve</source>
      <translation>æ—‹è½¬</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1335"/>
      <source>Revolves the selected sketch or profile around a line or axis and adds it to the body</source>
      <translation>å›´ç»•ä¸€æ¡çº¿æˆ–ä¸€ä¸ªè½´æ—‹è½¬é€‰å®šçš„è‰å›¾æˆ–è½®å»“ï¼Œå¹¶å°†å…¶æ·»åŠ åˆ°å®žä½“ä¸­</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignScaled</name>
    <message>
      <location filename="../../Command.cpp" line="2406"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2407"/>
      <source>Scale</source>
      <translation>ç¼©æ”¾</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2408"/>
      <source>Scales the selected features or the active body</source>
      <translation>ç¼©æ”¾é€‰å®šçš„ç‰¹å¾æˆ–æ´»åŠ¨å®žä½“</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignShapeBinder</name>
    <message>
      <location filename="../../Command.cpp" line="316"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="317"/>
      <source>Shape Binder</source>
      <translation>å½¢çŠ¶é“¾æŽ¥å™¨</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="318"/>
      <source>Creates a new shape binder</source>
      <translation>åˆ›å»ºä¸€ä¸ªæ–°çš„å½¢çŠ¶é“¾æŽ¥å™¨</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignSubShapeBinder</name>
    <message>
      <location filename="../../Command.cpp" line="386"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="387"/>
      <source>Sub-Shape Binder</source>
      <translation>å­å½¢çŠ¶å¼•ç”¨è¿žæŽ¥</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="388"/>
      <source>Creates a reference to geometry from one or more objects, allowing it to be used inside or outside a body. It tracks relative placements, supports multiple geometry types (solids, faces, edges, vertices), and can work with objects in the same or external documents.</source>
      <translation>åˆ›å»ºä¸€ä¸ªæˆ–å¤šä¸ªå¯¹è±¡çš„å‡ ä½•å¼•ç”¨ï¼Œå…è®¸å…¶åœ¨å®žä½“å†…å¤–ä½¿ç”¨ã€‚å®ƒè·Ÿè¸ªç›¸å¯¹ä½ç½®ï¼Œæ”¯æŒå¤šç§å‡ ä½•ç±»åž‹ï¼ˆå®žä½“ã€é¢ã€è¾¹ã€é¡¶ç‚¹ï¼‰ï¼Œå¹¶å¯ä¸ŽåŒä¸€æ–‡æ¡£æˆ–å¤–éƒ¨æ–‡æ¡£ä¸­çš„å¯¹è±¡åä½œã€‚</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignSubtractiveHelix</name>
    <message>
      <location filename="../../Command.cpp" line="1748"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1749"/>
      <source>Subtractive Helix</source>
      <translation>å‡æ–™èžºæ—‹</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1750"/>
      <source>Sweeps the selected sketch or profile along a helix and removes it from the body</source>
      <translation>æ²¿èžºæ—‹çº¿æ‰«æé€‰å®šçš„è‰å›¾æˆ–è½®å»“ï¼Œå¹¶å°†å…¶ä»Žå®žä½“ä¸­ç§»é™¤</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignSubtractiveLoft</name>
    <message>
      <location filename="../../Command.cpp" line="1615"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1616"/>
      <source>Subtractive Loft</source>
      <translation>å‡æ–™æ”¾æ ·</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1617"/>
      <source>Lofts the selected sketch or profile along a path and removes it from the body</source>
      <translation>æ²¿è·¯å¾„æ”¾æ ·é€‰å®šçš„è‰å›¾æˆ–è½®å»“ï¼Œå¹¶ä»Žå®žä½“ä¸­ç§»é™¤</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignSubtractivePipe</name>
    <message>
      <location filename="../../Command.cpp" line="1515"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1516"/>
      <source>Subtractive Pipe</source>
      <translation>å‡æ–™ç®¡é“</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1517"/>
      <source>Sweeps the selected sketch or profile along a path and removes it from the body</source>
      <translation>æ²¿è·¯å¾„æ‰«æé€‰å®šçš„è‰å›¾æˆ–è½®å»“ï¼Œå¹¶å°†å…¶ä»Žå®žä½“ä¸­ç§»é™¤</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignThickness</name>
    <message>
      <location filename="../../Command.cpp" line="2090"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2091"/>
      <source>Thickness</source>
      <translation>æŠ½å£³</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2092"/>
      <source>Applies thickness and removes the selected faces</source>
      <translation>åº”ç”¨åŽšåº¦å¹¶ç§»é™¤é€‰å®šçš„é¢</translation>
    </message>
  </context>
  <context>
    <name>CmdPrimtiveCompAdditive</name>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="76"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="77"/>
      <source>Additive Primitive</source>
      <translation>å¢žæ–™å›¾å…ƒ</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="78"/>
      <source>Creates an additive primitive</source>
      <translation>åˆ›å»ºå¢žæ–™å›¾å…ƒ</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="215"/>
      <source>Additive Box</source>
      <translation>å¢žæ–™ç«‹æ–¹ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="224"/>
      <source>Additive Cylinder</source>
      <translation>å¢žæ–™åœ†æŸ±ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="233"/>
      <source>Additive Sphere</source>
      <translation>å¢žæ–™çƒä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="242"/>
      <source>Additive Cone</source>
      <translation>å¢žæ–™åœ†é”¥ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="248"/>
      <source>Additive Ellipsoid</source>
      <translation>å¢žæ–™æ¤­çƒä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="254"/>
      <source>Additive Torus</source>
      <translation>å¢žæ–™åœ†çŽ¯ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="260"/>
      <source>Additive Prism</source>
      <translation>å¢žæ–™æ£±æŸ±ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="266"/>
      <source>Additive Wedge</source>
      <translation>å¢žæ–™æ¥”å½¢ä½“</translation>
    </message>
  </context>
  <context>
    <name>CmdPrimtiveCompSubtractive</name>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="284"/>
      <source>PartDesign</source>
      <translation>é›¶ä»¶è®¾è®¡</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="285"/>
      <source>Subtractive Primitive</source>
      <translation>å‡æ–™å›¾å…ƒ</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="286"/>
      <source>Creates a subtractive primitive</source>
      <translation>åˆ›å»ºä¸€ä¸ªå‡æ–™å›¾å…ƒ</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="400"/>
      <source>Subtractive Box</source>
      <translation>å‡æ–™ç«‹æ–¹ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="409"/>
      <source>Subtractive Cylinder</source>
      <translation>å‡æ–™åœ†æŸ±ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="418"/>
      <source>Subtractive Sphere</source>
      <translation>å‡æ–™çƒä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="427"/>
      <source>Subtractive Cone</source>
      <translation>å‡æ–™åœ†é”¥ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="433"/>
      <source>Subtractive Ellipsoid</source>
      <translation>å‡æ–™æ¤­çƒä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="439"/>
      <source>Subtractive Torus</source>
      <translation>å‡æ–™åœ†çŽ¯ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="445"/>
      <source>Subtractive Prism</source>
      <translation>å‡æ–™æ£±æŸ±ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="451"/>
      <source>Subtractive Wedge</source>
      <translation>å‡æ–™æ¥”å½¢ä½“</translation>
    </message>
  </context>
  <context>
    <name>Command</name>
    <message>
      <location filename="../../Command.cpp" line="338"/>
      <source>Edit Shape Binder</source>
      <translation>ç¼–è¾‘å½¢çŠ¶ç»‘å®šå™¨</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="349"/>
      <source>Create Shape Binder</source>
      <translation>åˆ›å»ºå½¢çŠ¶é“¾æŽ¥å™¨</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="442"/>
      <source>Create Sub-Shape Binder</source>
      <translation>åˆ›å»ºå­å½¢çŠ¶é“¾æŽ¥å™¨</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="512"/>
      <source>Create Clone</source>
      <translation>åˆ›å»ºå‰¯æœ¬</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1114"/>
      <source>Make Copy</source>
      <translation>åˆ›å»ºå‰¯æœ¬</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2504"/>
      <source>Convert to Multi-Transform feature</source>
      <translation>è½¬æ¢ä¸ºå¤šé‡å˜æ¢ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="255"/>
      <source>Sketch on Face</source>
      <translation>åœ¨é¢ä¸Šåˆ›å»ºè‰å›¾</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="316"/>
      <source>Make copy</source>
      <translation>åˆ¶ä½œå‰¯æœ¬</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="518"/>
      <location filename="../../SketchWorkflow.cpp" line="775"/>
      <source>New Sketch</source>
      <translation>æ–°å»ºè‰å›¾</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2601"/>
      <source>Create Boolean</source>
      <translation>åˆ›å»ºå¸ƒå°”å˜é‡</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="224"/>
      <location filename="../../DlgActiveBody.cpp" line="102"/>
      <source>Add a Body</source>
      <translation>æ·»åŠ å®žä½“</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="529"/>
      <source>Migrate legacy Part Design features to bodies</source>
      <translation>è¿ç§»æ—§ç‰ˆé›¶ä»¶è®¾è®¡ç‰¹å¾åˆ°å®žä½“</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="776"/>
      <source>Duplicate a Part Design object</source>
      <translation>å¤åˆ¶é›¶ä»¶è®¾è®¡å¯¹è±¡</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1121"/>
      <source>Move a feature inside body</source>
      <translation>ç§»åŠ¨ç‰¹å¾åˆ°å®žä½“ä¸­</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="730"/>
      <source>Move tip to selected feature</source>
      <translation>å°†ç»“ç®—ä½ç½®ç§»è‡³æ‰€é€‰ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="935"/>
      <source>Move an object</source>
      <translation>ç§»åŠ¨ä¸€ä¸ªå¯¹è±¡</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="261"/>
      <source>Mirror</source>
      <translation>é•œåƒ</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="301"/>
      <source>Linear Pattern</source>
      <translation>çº¿æ€§é˜µåˆ—</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="350"/>
      <source>Polar Pattern</source>
      <translation>çŽ¯å½¢é˜µåˆ—</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="389"/>
      <source>Scale</source>
      <translation>ç¼©æ”¾</translation>
    </message>
  </context>
  <context>
    <name>Gui::TaskView::TaskWatcherCommands</name>
    <message>
      <location filename="../../Workbench.cpp" line="55"/>
      <source>Face Tools</source>
      <translation>é¢å·¥å…·</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="56"/>
      <source>Edge Tools</source>
      <translation>è¾¹ç¼˜å·¥å…·</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="57"/>
      <source>Boolean Tools</source>
      <translation>å¸ƒå°”å·¥å…·</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="58"/>
      <source>Helper Tools</source>
      <translation>åŠ©æ‰‹</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="59"/>
      <source>Modeling Tools</source>
      <translation>å»ºæ¨¡å·¥å…·</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="60"/>
      <source>Create Geometry</source>
      <translation>åˆ›å»ºå‡ ä½•å…ƒç´ </translation>
    </message>
  </context>
  <context>
    <name>InvoluteGearParameter</name>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="14"/>
      <source>Involute Parameter</source>
      <translation>æ¸å¼€çº¿å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="20"/>
      <source>Number of teeth</source>
      <translation>é½¿æ•°</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="40"/>
      <source>Module</source>
      <translation>æ¨¡æ•°</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="84"/>
      <source>Pressure angle</source>
      <translation>åŽ‹åŠ›è§’</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="125"/>
      <source>High precision</source>
      <translation>é«˜ç²¾åº¦</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="139"/>
      <location filename="../../../InvoluteGearFeature.ui" line="166"/>
      <source>True</source>
      <translation>çœŸ</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="144"/>
      <location filename="../../../InvoluteGearFeature.ui" line="171"/>
      <source>False</source>
      <translation>å‡</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="152"/>
      <source>External gear</source>
      <translation>å¤–é½¿è½®</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="179"/>
      <source>Addendum coefficient</source>
      <translation>é½¿é¡¶é«˜ç³»æ•°</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="199"/>
      <source>Dedendum coefficient</source>
      <translation>é½¿æ ¹é«˜ç³»æ•°</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="219"/>
      <source>Root fillet coefficient</source>
      <translation>é½¿æ ¹åœ†è§’ç³»æ•°</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.ui" line="239"/>
      <source>Profile shift coefficient</source>
      <translation>é½¿å½¢å˜ä½ç³»æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::DlgActiveBody</name>
    <message>
      <location filename="../../DlgActiveBody.ui" line="14"/>
      <source>Active Body Required</source>
      <translation>éœ€è¦æ¿€æ´»çŠ¶æ€çš„å®žä½“</translation>
    </message>
    <message>
      <location filename="../../DlgActiveBody.ui" line="20"/>
      <source>To create a new Part Design object, there must be an active body in the document.
Select a body from below, or create a new body.</source>
      <translation>è¦åˆ›å»ºæ–°çš„é›¶ä»¶è®¾è®¡å¯¹è±¡ï¼Œæ–‡æ¡£ä¸­å¿…é¡»æœ‰ä¸€ä¸ªæ¿€æ´»çš„å®žä½“ã€‚
ä»Žä¸‹æ–¹é€‰æ‹©ä¸€ä¸ªå®žä½“ï¼Œæˆ–åˆ›å»ºä¸€ä¸ªæ–°å®žä½“ã€‚</translation>
    </message>
    <message>
      <location filename="../../DlgActiveBody.ui" line="35"/>
      <source>Create New Body</source>
      <translation>åˆ›å»ºæ–°å®žä½“</translation>
    </message>
    <message>
      <location filename="../../DlgActiveBody.cpp" line="53"/>
      <source>Please select</source>
      <translation>è¯·é€‰æ‹©</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::DlgPrimitives</name>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="14"/>
      <source>Geometric Primitives</source>
      <translation>å‡ ä½•å›¾å…ƒ</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="307"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="314"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1274"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1281"/>
      <source>Angle in first direction</source>
      <translation>ç¬¬ä¸€æ–¹å‘çš„è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="333"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="340"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1300"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1307"/>
      <source>Angle in second direction</source>
      <translation>ç¬¬äºŒæ–¹å‘çš„è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="62"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="153"/>
      <source>Length</source>
      <translation>é•¿åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="82"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="173"/>
      <source>Width</source>
      <translation>å®½åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="193"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="287"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="505"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1254"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1580"/>
      <source>Height</source>
      <translation>é«˜åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="267"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="625"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1600"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1749"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1805"/>
      <source>Radius</source>
      <translation>åŠå¾„</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="391"/>
      <source>Rotation angle</source>
      <translation>æ—‹è½¬è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="465"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="797"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1016"/>
      <source>Radius 1</source>
      <translation>åŠå¾„ 1</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="485"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="820"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1039"/>
      <source>Radius 2</source>
      <translation>åŠå¾„ 2</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="551"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1620"/>
      <source>Angle</source>
      <translation>è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="674"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="896"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1091"/>
      <source>U parameter</source>
      <translation>U å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="694"/>
      <source>V parameters</source>
      <translation>V å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="804"/>
      <source>Radius in local z-direction</source>
      <translation>æœ¬åœ°zæ–¹å‘çš„åŠå¾„</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="827"/>
      <source>Radius in local X-direction</source>
      <translation>å±€éƒ¨ X æ–¹å‘çš„åŠå¾„</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="843"/>
      <source>Radius 3</source>
      <translation>åŠå¾„ 3</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="850"/>
      <source>Radius in local Y-direction
If zero, it is equal to Radius2</source>
      <translation>å±€éƒ¨ Y æ–¹å‘çš„åŠå¾„
å¦‚æžœä¸ºé›¶ï¼Œåˆ™ç­‰äºŽåŠå¾„ 2</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="916"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1111"/>
      <source>V parameter</source>
      <translation>V å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1023"/>
      <source>Radius in local XY-plane</source>
      <translation>å±€éƒ¨ XY å¹³é¢çš„åŠå¾„</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1046"/>
      <source>Radius in local XZ-plane</source>
      <translation>å±€éƒ¨ XZ å¹³é¢çš„åŠå¾„</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1214"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="2290"/>
      <source>Polygon</source>
      <translation>å¤šè¾¹å½¢</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1234"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="2313"/>
      <source>Circumradius</source>
      <translation>å¤–æŽ¥åœ†åŠå¾„</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1353"/>
      <source>X min/max</source>
      <translation>X æœ€å°/æœ€å¤§</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1383"/>
      <source>Y min/max</source>
      <translation>Y æœ€å°/æœ€å¤§</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1413"/>
      <source>Z min/max</source>
      <translation>Z æœ€å°/æœ€å¤§</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1443"/>
      <source>X2 min/max</source>
      <translation>X2 æœ€å°/æœ€å¤§</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1476"/>
      <source>Z2 min/max</source>
      <translation>Z2 æœ€å°/æœ€å¤§</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1560"/>
      <source>Pitch</source>
      <translation>èŠ‚è·</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1637"/>
      <source>Coordinate system</source>
      <translation>åæ ‡ç³»</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1709"/>
      <source>Growth</source>
      <translation>å¢žé•¿</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1729"/>
      <source>Number of rotations</source>
      <translation>æ—‹è½¬æ¬¡æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1825"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1947"/>
      <source>Angle 1</source>
      <translation>è§’åº¦ 1</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1842"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="1964"/>
      <source>Angle 2</source>
      <translation>è§’åº¦ 2</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1879"/>
      <source>From 3 Points</source>
      <translation>é€šè¿‡ 3 ç‚¹å®šä¹‰</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1907"/>
      <source>Major radius</source>
      <translation>ä¸»åŠå¾„</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1927"/>
      <source>Minor radius</source>
      <translation>æ¬¡åŠå¾„</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="2005"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="2093"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="2170"/>
      <source>X</source>
      <translation>X</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="2025"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="2113"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="2193"/>
      <source>Y</source>
      <translation>Y</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="2045"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="2133"/>
      <location filename="../../TaskPrimitiveParameters.ui" line="2216"/>
      <source>Z</source>
      <translation>Z</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1645"/>
      <source>Right-handed</source>
      <translation>å³æ‰‹</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="1650"/>
      <source>Left-handed</source>
      <translation>å·¦æ‰‹</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="2086"/>
      <source>Start point</source>
      <translation>èµ·ç‚¹</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.ui" line="2160"/>
      <source>End point</source>
      <translation>ç»ˆç‚¹</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::DlgReference</name>
    <message>
      <location filename="../../DlgReference.ui" line="14"/>
      <source>Reference</source>
      <translation>å‚è€ƒ</translation>
    </message>
    <message>
      <location filename="../../DlgReference.ui" line="20"/>
      <source>You selected geometries which are not part of the active body. Please define how to handle those selections. If you do not want those references, cancel the command.</source>
      <translation>é€‰æ‹©çš„å‡ ä½•ä½“ä¸æ˜¯æ´»åŠ¨çš„å®žä½“çš„ä¸€éƒ¨åˆ†ã€‚è¯·æ˜Žç¡®å¦‚ä½•å¤„ç†è¿™äº›é€‰æ‹©ã€‚å¦‚æžœæ”¾å¼ƒç¼–è¾‘ï¼Œè¯·å–æ¶ˆæŒ‡ä»¤ã€‚</translation>
    </message>
    <message>
      <location filename="../../DlgReference.ui" line="42"/>
      <source>Make independent copy (recommended)</source>
      <translation>åˆ›å»ºç‹¬ç«‹å‰¯æœ¬ (æŽ¨è)</translation>
    </message>
    <message>
      <location filename="../../DlgReference.ui" line="52"/>
      <source>Make dependent copy</source>
      <translation>åˆ›å»ºå…³è”å‰¯æœ¬</translation>
    </message>
    <message>
      <location filename="../../DlgReference.ui" line="59"/>
      <source>Create cross-reference</source>
      <translation>åˆ›å»ºäº¤å‰å¼•ç”¨</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::NoDependentsSelection</name>
    <message>
      <location filename="../../ReferenceSelection.cpp" line="287"/>
      <source>Selecting this will cause circular dependency.</source>
      <translation>é€‰æ‹©æ“ä½œä¼šå¯¼è‡´å¾ªçŽ¯å¼•ç”¨ã€‚</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskBooleanParameters</name>
    <message>
      <location filename="../../TaskBooleanParameters.ui" line="22"/>
      <source>Add Body</source>
      <translation>æ·»åŠ å®žä½“</translation>
    </message>
    <message>
      <location filename="../../TaskBooleanParameters.ui" line="32"/>
      <source>Remove Body</source>
      <translation>ç§»é™¤å®žä½“</translation>
    </message>
    <message>
      <location filename="../../TaskBooleanParameters.ui" line="48"/>
      <source>Fuse</source>
      <translation>ç»“åˆ</translation>
    </message>
    <message>
      <location filename="../../TaskBooleanParameters.ui" line="53"/>
      <source>Cut</source>
      <translation>å‰ªåˆ‡</translation>
    </message>
    <message>
      <location filename="../../TaskBooleanParameters.ui" line="58"/>
      <source>Common</source>
      <translation>äº¤é›†</translation>
    </message>
    <message>
      <location filename="../../TaskBooleanParameters.cpp" line="53"/>
      <source>Boolean Parameters</source>
      <translation>å¸ƒå°”å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskBooleanParameters.cpp" line="84"/>
      <source>Remove</source>
      <translation>ç§»é™¤</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskBoxPrimitives</name>
    <message>
      <location filename="../../TaskPrimitiveParameters.cpp" line="52"/>
      <source>Primitive Parameters</source>
      <translation>å›¾å…ƒå‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.cpp" line="944"/>
      <location filename="../../TaskPrimitiveParameters.cpp" line="952"/>
      <location filename="../../TaskPrimitiveParameters.cpp" line="960"/>
      <source>Invalid wedge parameters</source>
      <translation>æ— æ•ˆçš„è¯·æ±‚å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.cpp" line="945"/>
      <source>X min must not be equal to X max!</source>
      <translation>Xæœ€å°å€¼ä¸èƒ½ç­‰äºŽXæœ€å¤§å€¼ï¼</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.cpp" line="953"/>
      <source>Y min must not be equal to Y max!</source>
      <translation>Y æœ€å°å€¼ä¸èƒ½ç­‰äºŽY æœ€å¤§å€¼ï¼</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.cpp" line="961"/>
      <source>Z min must not be equal to Z max!</source>
      <translation>Zæœ€å°å€¼ä¸èƒ½ç­‰äºŽZæœ€å¤§å€¼ï¼</translation>
    </message>
    <message>
      <location filename="../../TaskPrimitiveParameters.cpp" line="1003"/>
      <source>Create primitive</source>
      <translation>åˆ›å»ºå›¾å…ƒ</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskChamferParameters</name>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="20"/>
      <source>Toggles between selection and preview mode</source>
      <translation>åœ¨é€‰æ‹©å’Œé¢„è§ˆæ¨¡å¼ä¹‹é—´åˆ‡æ¢</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="23"/>
      <source>Select</source>
      <translation>é€‰æ‹©</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="33"/>
      <source>- select an item to highlight it
- double-click on an item to see the chamfers</source>
      <translation>- é€‰æ‹©ä¸€ä¸ªé¡¹ç›®ä»¥é«˜äº®æ˜¾ç¤º
- åŒå‡»ä¸€ä¸ªé¡¹ç›®ä»¥æŸ¥çœ‹å…¶å€’è§’</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="48"/>
      <source>Type</source>
      <translation>ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="56"/>
      <source>Equal distance</source>
      <translation>ç­‰è·ï¼š</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="61"/>
      <source>Two distances</source>
      <translation>ä¸¤ä¸ªè·ç¦»</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="66"/>
      <source>Distance and angle</source>
      <translation>è·ç¦»å’Œè§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="79"/>
      <source>Flips the direction</source>
      <translation>ç¿»è½¬æ–¹å‘</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="119"/>
      <source>Use all edges</source>
      <translation>ä½¿ç”¨æ‰€æœ‰è¾¹</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="100"/>
      <source>Size</source>
      <translation>å¤§å°</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="146"/>
      <source>Size 2</source>
      <translation>å°ºå¯¸ 2</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.ui" line="179"/>
      <source>Angle</source>
      <translation>è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskChamferParameters.cpp" line="346"/>
      <source>Empty chamfer created!
</source>
      <translation>æ²¡æœ‰å€’è§’è¢«åˆ›å»ºï¼
</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskDlgBooleanParameters</name>
    <message>
      <location filename="../../TaskBooleanParameters.cpp" line="386"/>
      <source>Empty body list</source>
      <translation>ç©ºçš„å®žä½“åˆ—è¡¨</translation>
    </message>
    <message>
      <location filename="../../TaskBooleanParameters.cpp" line="386"/>
      <source>The body list cannot be empty</source>
      <translation>å®žä½“åˆ—è¡¨ä¸èƒ½ç©º</translation>
    </message>
    <message>
      <location filename="../../TaskBooleanParameters.cpp" line="407"/>
      <source>Boolean: Accept: Input error</source>
      <translation>å¸ƒå°”å€¼ï¼š æŽ¥å—ï¼š è¾“å…¥é”™è¯¯</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskDlgDatumParameters</name>
    <message>
      <location filename="../../TaskDatumParameters.cpp" line="107"/>
      <source>Incompatible Reference Set</source>
      <translation>ä¸å…¼å®¹çš„å¼•ç”¨é›†</translation>
    </message>
    <message>
      <location filename="../../TaskDatumParameters.cpp" line="109"/>
      <source>There is no attachment mode that fits the current set of references. If you choose to continue, the feature will remain where it is now, and will not be moved as the references change. Continue?</source>
      <translation>æ²¡æœ‰é€‚åˆå½“å‰å‚è€ƒé›†çš„é™„ç€æ¨¡å¼ã€‚å¦‚æžœæ‚¨é€‰æ‹©ç»§ç»­ï¼Œç‰¹å¾å°†ä¿æŒçŽ°æœ‰çŠ¶æ€ï¼Œä¸”å°†è¢«å®šä¹‰ä¸ºå‚ç…§æ›´æ”¹è€Œä¸è¢«ç§»åŠ¨ã€‚è¦ç»§ç»­å—ï¼Ÿ</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskDlgShapeBinder</name>
    <message>
      <location filename="../../TaskShapeBinder.cpp" line="443"/>
      <source>Input error</source>
      <translation>è¾“å…¥é”™è¯¯</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskDraftParameters</name>
    <message>
      <location filename="../../TaskDraftParameters.ui" line="20"/>
      <source>Toggles between selection and preview mode</source>
      <translation>åœ¨é€‰åŒºå’Œé¢„è§ˆæ¨¡å¼ä¸­åˆ‡æ¢</translation>
    </message>
    <message>
      <location filename="../../TaskDraftParameters.ui" line="23"/>
      <source>Select</source>
      <translation>é€‰æ‹©</translation>
    </message>
    <message>
      <location filename="../../TaskDraftParameters.ui" line="33"/>
      <source>- select an item to highlight it
- double-click on an item to see the drafts</source>
      <translation>- é€‰æ‹©ä¸€ä¸ªé¡¹ç›®æ¥çªå‡ºæ˜¾ç¤º
- åŒå‡»ä¸€ä¸ªé¡¹ç›®æ¥æŸ¥çœ‹è‰ç¨¿</translation>
    </message>
    <message>
      <location filename="../../TaskDraftParameters.ui" line="46"/>
      <source>Draft angle</source>
      <translation>æ‹”æ¨¡è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskDraftParameters.ui" line="79"/>
      <source>Neutral Plane</source>
      <translation>ä¸­æ€§é¢</translation>
    </message>
    <message>
      <location filename="../../TaskDraftParameters.ui" line="96"/>
      <source>Pull Direction</source>
      <translation>æ‹”æ¨¡æ–¹å‘</translation>
    </message>
    <message>
      <location filename="../../TaskDraftParameters.ui" line="111"/>
      <source>Reverse pull direction</source>
      <translation>åè½¬æ‹”æ¨¡æ–¹å‘</translation>
    </message>
    <message>
      <location filename="../../TaskDraftParameters.cpp" line="304"/>
      <source>Empty draft created!
</source>
      <translation>ç©ºæ‹”æ¨¡å·²åˆ›å»ºï¼
</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskDressUpParameters</name>
    <message>
      <location filename="../../TaskDressUpParameters.cpp" line="302"/>
      <source>Select</source>
      <translation>é€‰æ‹©</translation>
    </message>
    <message>
      <location filename="../../TaskDressUpParameters.cpp" line="307"/>
      <source>Confirm Selection</source>
      <translation>ç¡®è®¤é€‰æ‹©</translation>
    </message>
    <message>
      <location filename="../../TaskDressUpParameters.cpp" line="320"/>
      <source>Add All Edges</source>
      <translation>æ·»åŠ æ‰€æœ‰è¾¹</translation>
    </message>
    <message>
      <location filename="../../TaskDressUpParameters.cpp" line="326"/>
      <source>Adds all edges to the list box (only when in add selection mode)</source>
      <translation>å°†æ‰€æœ‰è¾¹æ·»åŠ åˆ°åˆ—è¡¨æ¡†ï¼ˆä»…åœ¨æ·»åŠ é€‰æ‹©æ¨¡å¼ä¸‹ï¼‰</translation>
    </message>
    <message>
      <location filename="../../TaskDressUpParameters.cpp" line="335"/>
      <source>Remove</source>
      <translation>ç§»é™¤</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskExtrudeParameters</name>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="1374"/>
      <source>No face selected</source>
      <translation>æœªé€‰æ‹©ä»»ä½•é¢</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="173"/>
      <location filename="../../TaskExtrudeParameters.cpp" line="1143"/>
      <source>Face</source>
      <translation>é¢</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="77"/>
      <source>Remove</source>
      <translation>ç§»é™¤</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="354"/>
      <source>Preview</source>
      <translation>é¢„è§ˆ</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="358"/>
      <source>Select Faces</source>
      <translation>é€‰æ‹©é¢</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="694"/>
      <source>Select referenceâ€¦</source>
      <translation>é€‰æ‹©å‚è€ƒâ€¦</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="604"/>
      <source>No shape selected</source>
      <translation>æ— é€‰å®šçš„å½¢çŠ¶</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="687"/>
      <source>Sketch normal</source>
      <translation>è‰å›¾æ³•å‘</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="690"/>
      <source>Face normal</source>
      <translation>é¢æ³•çº¿</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="698"/>
      <location filename="../../TaskExtrudeParameters.cpp" line="701"/>
      <source>Custom direction</source>
      <translation>è‡ªå®šä¹‰æ–¹å‘ï¼š</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="1090"/>
      <source>Click on a shape in the model</source>
      <translation>ç‚¹å‡»æ¨¡åž‹ä¸­çš„å½¢çŠ¶</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="1361"/>
      <source>One sided</source>
      <translation>å•ä¾§</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="1362"/>
      <source>Two sided</source>
      <translation>åŒä¾§</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="1363"/>
      <source>Symmetric</source>
      <translation>å¯¹ç§°</translation>
    </message>
    <message>
      <location filename="../../TaskExtrudeParameters.cpp" line="1369"/>
      <source>Click on a face in the model</source>
      <translation>ç‚¹å‡»æ¨¡åž‹ä¸­çš„ä¸€ä¸ªé¢</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskFeaturePick</name>
    <message>
      <location filename="../../TaskFeaturePick.ui" line="23"/>
      <source>Allow used features</source>
      <translation>å…è®¸å·²è¢«ä½¿ç”¨çš„ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.ui" line="30"/>
      <source>Allow External Features</source>
      <translation>å…è®¸å¤–éƒ¨ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.ui" line="42"/>
      <source>From other bodies of the same part</source>
      <translation>ä»Žç›¸åŒé›¶ä»¶çš„å…¶ä»–å®žä½“</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.ui" line="49"/>
      <source>From different parts or free features</source>
      <translation>æ¥è‡ªä¸åŒçš„é›¶ä»¶æˆ–è‡ªç”±ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.ui" line="66"/>
      <source>Make independent copy (recommended)</source>
      <translation>åˆ›å»ºç‹¬ç«‹å‰¯æœ¬ (æŽ¨è)</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.ui" line="79"/>
      <source>Make dependent copy</source>
      <translation>åˆ›å»ºä¾èµ–å‰¯æœ¬</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.ui" line="89"/>
      <source>Create cross-reference</source>
      <translation>åˆ›å»ºäº¤å‰å¼•ç”¨</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.cpp" line="69"/>
      <source>Valid</source>
      <translation>æœ‰æ•ˆ</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.cpp" line="71"/>
      <source>Invalid shape</source>
      <translation>æ— æ•ˆå½¢çŠ¶</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.cpp" line="73"/>
      <source>No wire in sketch</source>
      <translation>è‰å›¾ä¸­æ‰¾ä¸åˆ°çº¿æ¡†</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.cpp" line="75"/>
      <source>Sketch already used by other feature</source>
      <translation>è‰å›¾è¢«å…¶ä»–ç‰¹å¾ä½¿ç”¨</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.cpp" line="77"/>
      <source>Belongs to another body</source>
      <translation>å±žäºŽå¦ä¸€ä¸ªå®žä½“</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.cpp" line="79"/>
      <source>Belongs to another part</source>
      <translation>å±žäºŽå¦ä¸€ä¸ªé›¶ä»¶</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.cpp" line="81"/>
      <source>Doesn't belong to any body</source>
      <translation>ä¸å±žäºŽä»»ä½•å®žä½“</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.cpp" line="83"/>
      <source>Base plane</source>
      <translation>åŸºå‡†å¹³é¢</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.cpp" line="85"/>
      <source>Feature is located after the tip of the body</source>
      <translation>ç‰¹å¾ä½äºŽå®žä½“çš„æœ«ç«¯ä¹‹åŽ</translation>
    </message>
    <message>
      <location filename="../../TaskFeaturePick.cpp" line="97"/>
      <source>Select Attachment</source>
      <translation>é€‰æ‹©é™„ç€é¢</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskFilletParameters</name>
    <message>
      <location filename="../../TaskFilletParameters.ui" line="20"/>
      <source>Toggles between selection and preview mode</source>
      <translation>åœ¨é€‰æ‹©å’Œé¢„è§ˆæ¨¡å¼ä¹‹é—´åˆ‡æ¢</translation>
    </message>
    <message>
      <location filename="../../TaskFilletParameters.ui" line="23"/>
      <source>Select</source>
      <translation>é€‰æ‹©</translation>
    </message>
    <message>
      <location filename="../../TaskFilletParameters.ui" line="33"/>
      <source>- select an item to highlight it
- double-click on an item to see the fillets</source>
      <translation>- é€‰æ‹©ä¸€ä¸ªé¡¹ç›®æ¥çªå‡ºæ˜¾ç¤º
- åŒå‡»ä¸€ä¸ªé¡¹ç›®æ¥æŸ¥çœ‹è¿™äº›æ–‡ä»¶</translation>
    </message>
    <message>
      <location filename="../../TaskFilletParameters.ui" line="46"/>
      <source>Radius</source>
      <translation>åŠå¾„</translation>
    </message>
    <message>
      <location filename="../../TaskFilletParameters.ui" line="62"/>
      <source>Use all edges</source>
      <translation>ä½¿ç”¨æ‰€æœ‰è¾¹</translation>
    </message>
    <message>
      <location filename="../../TaskFilletParameters.cpp" line="205"/>
      <source>Empty fillet created!</source>
      <translation>ç©ºåœ†è§’å·²åˆ›å»ºï¼</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskHelixParameters</name>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="29"/>
      <source>Valid</source>
      <translation>æœ‰æ•ˆ</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="48"/>
      <location filename="../../TaskHelixParameters.cpp" line="241"/>
      <source>Base X-axis</source>
      <translation>X è½´</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="53"/>
      <location filename="../../TaskHelixParameters.cpp" line="242"/>
      <source>Base Y-axis</source>
      <translation>Y è½´</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="58"/>
      <location filename="../../TaskHelixParameters.cpp" line="243"/>
      <source>Base Z-axis</source>
      <translation>Z è½´</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="63"/>
      <location filename="../../TaskHelixParameters.cpp" line="225"/>
      <source>Horizontal sketch axis</source>
      <translation>æ°´å¹³è‰ç»˜è½´</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="68"/>
      <location filename="../../TaskHelixParameters.cpp" line="224"/>
      <source>Vertical sketch axis</source>
      <translation>åž‚ç›´è‰ç»˜è½´</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="73"/>
      <location filename="../../TaskHelixParameters.cpp" line="223"/>
      <source>Normal sketch axis</source>
      <translation type="unfinished">Normal sketch axis</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="22"/>
      <source>Status</source>
      <translation>çŠ¶æ€</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="40"/>
      <source>Axis</source>
      <translation>è½´çº¿</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="78"/>
      <location filename="../../TaskHelixParameters.cpp" line="208"/>
      <source>Select referenceâ€¦</source>
      <translation>é€‰æ‹©å‚è€ƒâ€¦</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="90"/>
      <source>Mode</source>
      <translation>æ¨¡å¼</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="98"/>
      <source>Pitch-Height-Angle</source>
      <translation>èŠ‚è·-é«˜åº¦-è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="103"/>
      <source>Pitch-Turns-Angle</source>
      <translation>èŠ‚è·-åœˆæ•°-è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="108"/>
      <source>Height-Turns-Angle</source>
      <translation>é«˜-åœˆæ•°-è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="113"/>
      <source>Height-Turns-Growth</source>
      <translation>é«˜-åœˆæ•°-å¢žé•¿</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="125"/>
      <source>Pitch</source>
      <translation>èŠ‚è·</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="152"/>
      <source>Height</source>
      <translation>é«˜åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="179"/>
      <source>Turns</source>
      <translation>åœˆæ•°</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="203"/>
      <source>Cone angle</source>
      <translation>åœ†é”¥è§’</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="233"/>
      <source>Radial growth</source>
      <translation>å¾„å‘å¢žé•¿</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="289"/>
      <source>Recompute on change</source>
      <translation>æ›´æ”¹æ—¶é‡æ–°è®¡ç®—</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="255"/>
      <source>Left handed</source>
      <translation>å·¦æ—‹</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="265"/>
      <source>Reversed</source>
      <translation>åè½¬</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.ui" line="272"/>
      <source>Remove outside of profile</source>
      <translation>åˆ é™¤é…ç½®ä¹‹å¤–çš„æ–‡ä»¶</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.cpp" line="57"/>
      <source>Helix Parameters</source>
      <translation>èžºæ—‹å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.cpp" line="227"/>
      <source>Construction line %1</source>
      <translation>è¾…åŠ©çº¿ %1</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.cpp" line="295"/>
      <source>Warning: helix might be self intersecting</source>
      <translation>è­¦å‘Šï¼šèžºæ—‹å¯èƒ½æ˜¯è‡ªäº¤çš„</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.cpp" line="300"/>
      <source>Error: helix touches itself</source>
      <translation>é”™è¯¯: èžºæ—‹è‡ªç›¸äº¤</translation>
    </message>
    <message>
      <location filename="../../TaskHelixParameters.cpp" line="349"/>
      <source>Error: unsupported mode</source>
      <translation>é”™è¯¯ï¼šä¸æ”¯æŒçš„æ¨¡å¼</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskHoleParameters</name>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="57"/>
      <source>Counterbore</source>
      <translation>æ²‰å­”</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="58"/>
      <source>Countersink</source>
      <translation>åŸ‹å¤´å­”</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="59"/>
      <source>Counterdrill</source>
      <translation>æ²‰å¤´é’»</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="63"/>
      <source>Hole Parameters</source>
      <translation>å­”å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="72"/>
      <source>None</source>
      <translation>æ— </translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="73"/>
      <source>ISO metric regular</source>
      <translation>ISO ç±³åˆ¶æ™®é€šèžºçº¹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="74"/>
      <source>ISO metric fine</source>
      <translation>ISO ç±³åˆ¶ç»†ç‰™èžºçº¹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="75"/>
      <source>UTS coarse</source>
      <translation>UTS ç»Ÿä¸€ç²—ç‰™èžºçº¹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="76"/>
      <source>UTS fine</source>
      <translation>UTS ç»Ÿä¸€ç»†ç‰™èžºçº¹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="77"/>
      <source>UTS extra fine</source>
      <translation>UTS ç»Ÿä¸€è¶…ç»†ç‰™èžºçº¹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="78"/>
      <source>ANSI pipes</source>
      <translation>ANSI ç¾Žæ ‡ç®¡èžºçº¹æ ‡å‡†</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="79"/>
      <source>ISO/BSP pipes</source>
      <translation>ISO/BSP å›½é™…/è‹±æ ‡ç®¡èžºçº¹æ ‡å‡†</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="80"/>
      <source>BSW whitworth</source>
      <translation>BSW æƒ æ°èžºçº¹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="81"/>
      <source>BSF whitworth fine</source>
      <translation>BSF æƒ æ°ç»†ç‰™èžºçº¹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="82"/>
      <source>ISO tyre valves</source>
      <translation>ISO è½®èƒŽæ°”é—¨å˜´</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="712"/>
      <source>Medium</source>
      <comment>Distance between thread crest and hole wall, use ISO-273 nomenclature or equivalent if possible</comment>
      <translation>ä¸­</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="716"/>
      <source>Fine</source>
      <comment>Distance between thread crest and hole wall, use ISO-273 nomenclature or equivalent if possible</comment>
      <translation>ç²¾ç»†</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="720"/>
      <source>Coarse</source>
      <comment>Distance between thread crest and hole wall, use ISO-273 nomenclature or equivalent if possible</comment>
      <translation>ç²—ç³™</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="726"/>
      <source>Normal</source>
      <comment>Distance between thread crest and hole wall, use ASME B18.2.8 nomenclature or equivalent if possible</comment>
      <translation>æ³•å‘</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="730"/>
      <source>Close</source>
      <comment>Distance between thread crest and hole wall, use ASME B18.2.8 nomenclature or equivalent if possible</comment>
      <translation>å…³é—­</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="734"/>
      <source>Loose</source>
      <comment>Distance between thread crest and hole wall, use ASME B18.2.8 nomenclature or equivalent if possible</comment>
      <translation>å®½æ¾</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="738"/>
      <source>Normal</source>
      <comment>Distance between thread crest and hole wall</comment>
      <translation>æ³•å‘</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="739"/>
      <source>Close</source>
      <comment>Distance between thread crest and hole wall</comment>
      <translation>å…³é—­</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.cpp" line="740"/>
      <source>Wide</source>
      <comment>Distance between thread crest and hole wall</comment>
      <translation>å®½åº¦</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskLoftParameters</name>
    <message>
      <location filename="../../TaskLoftParameters.ui" line="20"/>
      <source>Ruled surface</source>
      <translation>ç›´çº¹é¢</translation>
    </message>
    <message>
      <location filename="../../TaskLoftParameters.ui" line="27"/>
      <source>Closed</source>
      <translation>å…³é—­</translation>
    </message>
    <message>
      <location filename="../../TaskLoftParameters.ui" line="34"/>
      <source>Profile</source>
      <translation>è½®å»“</translation>
    </message>
    <message>
      <location filename="../../TaskLoftParameters.ui" line="42"/>
      <source>Object</source>
      <translation>å¯¹è±¡</translation>
    </message>
    <message>
      <location filename="../../TaskLoftParameters.ui" line="65"/>
      <source>Add Section</source>
      <translation>æ·»åŠ æˆªé¢</translation>
    </message>
    <message>
      <location filename="../../TaskLoftParameters.ui" line="78"/>
      <source>Remove Section</source>
      <translation>åˆ é™¤æˆªé¢</translation>
    </message>
    <message>
      <location filename="../../TaskLoftParameters.ui" line="103"/>
      <source>List can be reordered by dragging</source>
      <translation>åˆ—è¡¨å¯ä»¥é€šè¿‡æ‹–åŠ¨é‡æ–°æŽ’åº</translation>
    </message>
    <message>
      <location filename="../../TaskLoftParameters.ui" line="120"/>
      <source>Recompute on change</source>
      <translation>æ›´æ”¹æ—¶é‡æ–°è®¡ç®—</translation>
    </message>
    <message>
      <location filename="../../TaskLoftParameters.cpp" line="50"/>
      <source>Loft Parameters</source>
      <translation>æ”¾æ ·å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskLoftParameters.cpp" line="74"/>
      <source>Remove</source>
      <translation>ç§»é™¤</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskMirroredParameters</name>
    <message>
      <location filename="../../TaskMirroredParameters.ui" line="34"/>
      <source>Plane</source>
      <translation>å¹³é¢</translation>
    </message>
    <message>
      <location filename="../../TaskMirroredParameters.cpp" line="186"/>
      <source>Error</source>
      <translation>é”™è¯¯</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskMultiTransformParameters</name>
    <message>
      <location filename="../../TaskMultiTransformParameters.ui" line="32"/>
      <source>Transformations</source>
      <translation>å˜æ¢</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.ui" line="52"/>
      <source>OK</source>
      <translation>ç¡®å®š</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="71"/>
      <source>Edit</source>
      <translation>ç¼–è¾‘</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="74"/>
      <source>Delete</source>
      <translation>åˆ é™¤</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="77"/>
      <source>Add Mirror Transformation</source>
      <translation>æ·»åŠ é•œåƒå˜æ¢</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="85"/>
      <source>Add Linear Pattern</source>
      <translation>æ·»åŠ çº¿æ€§é˜µåˆ—</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="93"/>
      <source>Add Polar Pattern</source>
      <translation>æ·»åŠ æžè½´é˜µåˆ—</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="101"/>
      <source>Add Scale Transformation</source>
      <translation>æ·»åŠ ç¼©æ”¾å˜æ¢</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="104"/>
      <source>Move Up</source>
      <translation>ä¸Šç§»</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="107"/>
      <source>Move Down</source>
      <translation>ä¸‹ç§»</translation>
    </message>
    <message>
      <location filename="../../TaskMultiTransformParameters.cpp" line="139"/>
      <source>Right-click to add a transformation</source>
      <translation>å³é”®å•å‡»ä»¥æ·»åŠ å˜æ¢</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskPadParameters</name>
    <message>
      <location filename="../../TaskPadParameters.cpp" line="40"/>
      <source>Pad Parameters</source>
      <translation>å‡¸å°å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskPadParameters.cpp" line="42"/>
      <source>Offset the pad from the face at which the pad will end on side 1</source>
      <translation>ä»Žåž«ç‰‡å°†åœ¨ä¾§é¢ 1 ç»“æŸçš„é¢åç§»åž«ç‰‡</translation>
    </message>
    <message>
      <location filename="../../TaskPadParameters.cpp" line="43"/>
      <source>Offset the pad from the face at which the pad will end on side 2</source>
      <translation>ä»Žåž«ç‰‡å°†åœ¨ä¾§é¢ 2 ç»“æŸçš„é¢åç§»åž«ç‰‡</translation>
    </message>
    <message>
      <location filename="../../TaskPadParameters.cpp" line="44"/>
      <source>Reverses pad direction</source>
      <translation>åè½¬å‡¸å°æ–¹å‘</translation>
    </message>
    <message>
      <location filename="../../TaskPadParameters.cpp" line="73"/>
      <source>Dimension</source>
      <translation>å°ºå¯¸æ ‡æ³¨</translation>
    </message>
    <message>
      <location filename="../../TaskPadParameters.cpp" line="74"/>
      <source>To last</source>
      <translation>ç›´åˆ°æœ€åŽ</translation>
    </message>
    <message>
      <location filename="../../TaskPadParameters.cpp" line="75"/>
      <source>To first</source>
      <translation>åˆ°èµ·å§‹ä½ç½®</translation>
    </message>
    <message>
      <location filename="../../TaskPadParameters.cpp" line="76"/>
      <source>Up to face</source>
      <translation>ç›´åˆ°è¡¨é¢</translation>
    </message>
    <message>
      <location filename="../../TaskPadParameters.cpp" line="77"/>
      <source>Up to shape</source>
      <translation>ä¸Šè‡³å½¢çŠ¶</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskPadPocketParameters</name>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="68"/>
      <location filename="../../TaskPadPocketParameters.ui" line="303"/>
      <source>Type</source>
      <translation>ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="76"/>
      <source>Dimension</source>
      <translation>å°ºå¯¸</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="84"/>
      <location filename="../../TaskPadPocketParameters.ui" line="313"/>
      <source>Length</source>
      <translation>é•¿åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="101"/>
      <location filename="../../TaskPadPocketParameters.ui" line="330"/>
      <source>Offset to face</source>
      <translation>ç›¸å¯¹äºŽé¢åç§»</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="192"/>
      <location filename="../../TaskPadPocketParameters.ui" line="421"/>
      <source>Select all faces</source>
      <translation>é€‰å–æ‰€æœ‰é¢</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="217"/>
      <location filename="../../TaskPadPocketParameters.ui" line="446"/>
      <source>Select</source>
      <translation>é€‰æ‹©</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="255"/>
      <location filename="../../TaskPadPocketParameters.ui" line="484"/>
      <source>Select Face</source>
      <translation>é€‰æ‹©é¢</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="281"/>
      <source>Side 2</source>
      <translation>ä¾§é¢ 2</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="512"/>
      <source>Direction</source>
      <translation>æ–¹å‘</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="541"/>
      <source>Set a direction or select an edge
from the model as reference</source>
      <translation>è®¾ç½®ä¸€ä¸ªæ–¹å‘æˆ–ä»Žæ¨¡åž‹ä¸­é€‰æ‹©è¾¹
ä½œä¸ºå‚è€ƒå€¼</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="546"/>
      <source>Sketch normal</source>
      <translation>è‰å›¾æ³•å‘</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="556"/>
      <source>Custom direction</source>
      <translation>è‡ªå®šä¹‰æ–¹å‘ï¼š</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="569"/>
      <source>Use custom vector for pad direction, otherwise
the sketch plane's normal vector will be used</source>
      <translation>å¦åˆ™ï¼Œè¯·å°†è‡ªå®šä¹‰å‘é‡ç”¨äºŽå‡¸å°æ–¹å‘
å°†ä½¿ç”¨è‰å›¾å¹³é¢çš„æ³•å‘é‡</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="521"/>
      <source>If unchecked, the length will be
measured along the specified direction</source>
      <translation>å¦‚æžœä¸é€‰ä¸­ï¼Œé•¿åº¦å°†æŒ‰ç…§æŒ‡å®šçš„æ–¹å‘è¿›è¡Œæµ‹é‡</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="525"/>
      <source>Length along sketch normal</source>
      <translation>æ²¿è‰å›¾æ³•çº¿é•¿åº¦ï¼š</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="214"/>
      <location filename="../../TaskPadPocketParameters.ui" line="443"/>
      <source>Toggles between selection and preview mode</source>
      <translation>åœ¨é€‰æ‹©å’Œé¢„è§ˆæ¨¡å¼ä¹‹é—´åˆ‡æ¢</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="505"/>
      <source>Reversed</source>
      <translation>åè½¬</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="534"/>
      <source>Direction/edge</source>
      <translation>æ–¹å‘/è¾¹ç¼˜</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="551"/>
      <source>Select referenceâ€¦</source>
      <translation>é€‰æ‹©å‚è€ƒâ€¦</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="582"/>
      <source>X</source>
      <translation>X</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="589"/>
      <source>X-component of direction vector</source>
      <translation>æ–¹å‘å‘é‡çš„ X åˆ†é‡</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="611"/>
      <source>Y</source>
      <translation>Y</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="618"/>
      <source>Y-component of direction vector</source>
      <translation>æ–¹å‘å‘é‡çš„ Y åˆ†é‡</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="640"/>
      <source>Z</source>
      <translation>Z</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="647"/>
      <source>Z-component of direction vector</source>
      <translation>æ–¹å‘å‘é‡çš„ Z åˆ†é‡</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="118"/>
      <location filename="../../TaskPadPocketParameters.ui" line="347"/>
      <source>Angle to taper the extrusion</source>
      <translation>å€¾æ–œæ‹‰ä¼¸çš„è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="22"/>
      <source>Mode</source>
      <translation>æ¨¡å¼</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="46"/>
      <source>Side 1</source>
      <translation>ä¾§é¢ 1</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="121"/>
      <location filename="../../TaskPadPocketParameters.ui" line="350"/>
      <source>Taper angle</source>
      <translation>é”¥åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="174"/>
      <location filename="../../TaskPadPocketParameters.ui" line="403"/>
      <source>Select Shape</source>
      <translation>é€‰æ‹©å½¢çŠ¶</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="189"/>
      <location filename="../../TaskPadPocketParameters.ui" line="418"/>
      <source>Selects all faces of the shape</source>
      <translation>é€‰æ‹©å½¢çŠ¶çš„æ‰€æœ‰é¢</translation>
    </message>
    <message>
      <location filename="../../TaskPadPocketParameters.ui" line="678"/>
      <source>Recompute on change</source>
      <translation>æ›´æ”¹æ—¶é‡æ–°è®¡ç®—</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskPipeOrientation</name>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="22"/>
      <source>Orientation mode</source>
      <translation>æ–¹å‘æ¨¡å¼</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="36"/>
      <source>Standard</source>
      <translation>æ ‡å‡†</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="41"/>
      <source>Fixed</source>
      <translation>å›ºå®š</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="46"/>
      <source>Frenet</source>
      <translation>Frenet</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="51"/>
      <source>Auxiliary</source>
      <translation>è¾…åŠ©</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="56"/>
      <source>Binormal</source>
      <translation>å‰¯æ³•çº¿</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="76"/>
      <source>Curvilinear equivalence</source>
      <translation>æ›²çº¿ç­‰æ•ˆæ€§</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="83"/>
      <source>Profile</source>
      <translation>è½®å»“</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="91"/>
      <source>Object</source>
      <translation>å¯¹è±¡</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="125"/>
      <source>Add Edge</source>
      <translation>æ·»åŠ è¾¹</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="144"/>
      <source>Remove Edge</source>
      <translation>åˆ é™¤è¾¹</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="166"/>
      <source>Set the constant binormal vector used to calculate the profiles orientation</source>
      <translation>è®¾ç½®ç”¨äºŽè®¡ç®—è½®å»“æ–¹å‘çš„å¸¸é‡å‰¯æ³•å‘é‡</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="190"/>
      <source>X</source>
      <translation>X</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="197"/>
      <source>Y</source>
      <translation>Y</translation>
    </message>
    <message>
      <location filename="../../TaskPipeOrientation.ui" line="204"/>
      <source>Z</source>
      <translation>Z</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.cpp" line="598"/>
      <source>Section Orientation</source>
      <translation>æˆªé¢æ–¹å‘</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.cpp" line="626"/>
      <source>Remove</source>
      <translation>ç§»é™¤</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskPipeParameters</name>
    <message>
      <location filename="../../TaskPipeParameters.ui" line="20"/>
      <source>Profile</source>
      <translation>è½®å»“</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.ui" line="28"/>
      <location filename="../../TaskPipeParameters.ui" line="93"/>
      <source>Object</source>
      <translation>å¯¹è±¡</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.ui" line="51"/>
      <source>Corner transition</source>
      <translation>æ‹è§’è¿‡æ¸¡</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.ui" line="70"/>
      <source>Right corner</source>
      <translation>å³æ‹è§’</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.ui" line="75"/>
      <source>Round corner</source>
      <translation>åœ†è§’</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.ui" line="85"/>
      <source>Path to Sweep Along</source>
      <translation>æ‰«æŽ è·¯å¾„</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.ui" line="119"/>
      <source>Add edge</source>
      <translation>æ·»åŠ è¾¹ç¼˜</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.ui" line="138"/>
      <source>Remove edge</source>
      <translation>ç§»é™¤è¾¹ç¼˜</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.ui" line="65"/>
      <source>Transformed</source>
      <translation>å˜æ¢</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.cpp" line="69"/>
      <source>Pipe Parameters</source>
      <translation>ç®¡é“å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.cpp" line="80"/>
      <source>Select All</source>
      <translation>å…¨é€‰</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.cpp" line="98"/>
      <source>Remove</source>
      <translation>ç§»é™¤</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.cpp" line="463"/>
      <location filename="../../TaskPipeParameters.cpp" line="584"/>
      <source>Input error</source>
      <translation>è¾“å…¥é”™è¯¯</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.cpp" line="463"/>
      <source>No active body</source>
      <translation>æ²¡æœ‰æ´»åŠ¨çš„å®žä½“</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskPipeScaling</name>
    <message>
      <location filename="../../TaskPipeScaling.ui" line="22"/>
      <source>Transform mode</source>
      <translation>å˜æ¢æ¨¡å¼</translation>
    </message>
    <message>
      <location filename="../../TaskPipeScaling.ui" line="36"/>
      <source>Constant</source>
      <translation>å¸¸é‡</translation>
    </message>
    <message>
      <location filename="../../TaskPipeScaling.ui" line="41"/>
      <source>Multisection</source>
      <translation>å¤šæˆªé¢</translation>
    </message>
    <message>
      <location filename="../../TaskPipeScaling.ui" line="64"/>
      <source>Add Section</source>
      <translation>æ·»åŠ æˆªé¢</translation>
    </message>
    <message>
      <location filename="../../TaskPipeScaling.ui" line="77"/>
      <source>Remove Section</source>
      <translation>åˆ é™¤æˆªé¢</translation>
    </message>
    <message>
      <location filename="../../TaskPipeScaling.ui" line="102"/>
      <source>List can be reordered by dragging</source>
      <translation>åˆ—è¡¨å¯ä»¥é€šè¿‡æ‹–åŠ¨é‡æ–°æŽ’åº</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.cpp" line="897"/>
      <source>Section Transformation</source>
      <translation>æˆªé¢å˜æ¢</translation>
    </message>
    <message>
      <location filename="../../TaskPipeParameters.cpp" line="916"/>
      <source>Remove</source>
      <translation>ç§»é™¤</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskPocketParameters</name>
    <message>
      <location filename="../../TaskPocketParameters.cpp" line="40"/>
      <source>Pocket Parameters</source>
      <translation>å‡¹æ§½å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskPocketParameters.cpp" line="43"/>
      <source>Offset from the selected face at which the pocket will end on side 1</source>
      <translation>ä»Žé€‰å®šçš„é¢åç§»ï¼Œå£è¢‹å°†åœ¨ä¾§é¢ 1 ç»“æŸ</translation>
    </message>
    <message>
      <location filename="../../TaskPocketParameters.cpp" line="46"/>
      <source>Offset from the selected face at which the pocket will end on side 2</source>
      <translation>ä»Žé€‰å®šçš„é¢åç§»ï¼Œå£è¢‹å°†åœ¨ä¾§é¢ 2 ç»“æŸ</translation>
    </message>
    <message>
      <location filename="../../TaskPocketParameters.cpp" line="48"/>
      <source>Reverses pocket direction</source>
      <translation>åè½¬å‡¹æ§½æ–¹å‘</translation>
    </message>
    <message>
      <location filename="../../TaskPocketParameters.cpp" line="77"/>
      <source>Dimension</source>
      <translation>å°ºå¯¸</translation>
    </message>
    <message>
      <location filename="../../TaskPocketParameters.cpp" line="78"/>
      <source>Through all</source>
      <translation>é€šè¿‡æ‰€æœ‰</translation>
    </message>
    <message>
      <location filename="../../TaskPocketParameters.cpp" line="79"/>
      <source>To first</source>
      <translation>åˆ°èµ·å§‹ä½ç½®</translation>
    </message>
    <message>
      <location filename="../../TaskPocketParameters.cpp" line="80"/>
      <source>Up to face</source>
      <translation>ç›´åˆ°é¢</translation>
    </message>
    <message>
      <location filename="../../TaskPocketParameters.cpp" line="81"/>
      <source>Up to shape</source>
      <translation>ä¸Šè‡³å½¢çŠ¶</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskRevolutionParameters</name>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="22"/>
      <source>Type</source>
      <translation>ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="50"/>
      <location filename="../../TaskRevolutionParameters.cpp" line="222"/>
      <source>Base X-axis</source>
      <translation>X è½´</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="55"/>
      <location filename="../../TaskRevolutionParameters.cpp" line="223"/>
      <source>Base Y-axis</source>
      <translation>Y è½´</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="60"/>
      <location filename="../../TaskRevolutionParameters.cpp" line="224"/>
      <source>Base Z-axis</source>
      <translation>Z è½´</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="65"/>
      <source>Horizontal sketch axis</source>
      <translation>æ°´å¹³è‰ç»˜è½´</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="70"/>
      <source>Vertical sketch axis</source>
      <translation>åž‚ç›´è‰ç»˜è½´</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="154"/>
      <source>Symmetric to plane</source>
      <translation>ç›¸å½“å¹³é¢å¯¹ç§°</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="161"/>
      <source>Reversed</source>
      <translation>åè½¬</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="120"/>
      <source>2nd angle</source>
      <translation>ç¬¬äºŒè§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="42"/>
      <source>Axis</source>
      <translation>è½´çº¿</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="75"/>
      <location filename="../../TaskRevolutionParameters.cpp" line="232"/>
      <source>Select referenceâ€¦</source>
      <translation>é€‰æ‹©å‚è€ƒâ€¦</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="87"/>
      <location filename="../../TaskRevolutionParameters.cpp" line="175"/>
      <source>Angle</source>
      <translation>è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="170"/>
      <location filename="../../TaskRevolutionParameters.cpp" line="149"/>
      <location filename="../../TaskRevolutionParameters.cpp" line="459"/>
      <source>Face</source>
      <translation>é¢</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.ui" line="192"/>
      <source>Recompute on change</source>
      <translation>æ›´æ”¹æ—¶é‡æ–°è®¡ç®—</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.cpp" line="177"/>
      <source>To last</source>
      <translation>ç›´åˆ°æœ€åŽ</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.cpp" line="180"/>
      <source>Through all</source>
      <translation>é€šè¿‡æ‰€æœ‰</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.cpp" line="182"/>
      <source>To first</source>
      <translation>åˆ°èµ·å§‹ä½ç½®</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.cpp" line="183"/>
      <source>Up to face</source>
      <translation>ç›´åˆ°é¢</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.cpp" line="184"/>
      <source>Two angles</source>
      <translation>ä¸¤ä¸ªè§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.cpp" line="447"/>
      <source>No face selected</source>
      <translation>æœªé€‰æ‹©ä»»ä½•é¢</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskScaledParameters</name>
    <message>
      <location filename="../../TaskScaledParameters.ui" line="34"/>
      <source>Factor</source>
      <translation>ç¼©æ”¾å› å­</translation>
    </message>
    <message>
      <location filename="../../TaskScaledParameters.ui" line="48"/>
      <source>Occurrences</source>
      <translation>å‡ºçŽ°æ¬¡æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskShapeBinder</name>
    <message>
      <location filename="../../TaskShapeBinder.ui" line="22"/>
      <source>Object</source>
      <translation>å¯¹è±¡</translation>
    </message>
    <message>
      <location filename="../../TaskShapeBinder.ui" line="48"/>
      <source>Add Geometry</source>
      <translation>æ·»åŠ å‡ ä½•å›¾å½¢</translation>
    </message>
    <message>
      <location filename="../../TaskShapeBinder.ui" line="67"/>
      <source>Remove Geometry</source>
      <translation>ç§»é™¤å‡ ä½•å›¾å½¢</translation>
    </message>
    <message>
      <location filename="../../TaskShapeBinder.cpp" line="61"/>
      <source>Shape Binder Parameters</source>
      <translation>å½¢çŠ¶ç»‘å®šå™¨å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskShapeBinder.cpp" line="139"/>
      <source>Remove</source>
      <translation>ç§»é™¤</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskSketchBasedParameters</name>
    <message>
      <location filename="../../TaskSketchBasedParameters.cpp" line="204"/>
      <source>Face</source>
      <translation>é¢</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskThicknessParameters</name>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="20"/>
      <source>Toggles between selection and preview mode</source>
      <translation>åœ¨é€‰æ‹©å’Œé¢„è§ˆæ¨¡å¼ä¹‹é—´åˆ‡æ¢</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="23"/>
      <source>Select</source>
      <translation>é€‰æ‹©</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="33"/>
      <source>- select an item to highlight it
- double-click on an item to see the features</source>
      <translation>- é€‰æ‹©ä¸€ä¸ªé¡¹ç›®æ¥çªå‡ºæ˜¾ç¤º
- åŒå‡»ä¸€ä¸ªé¡¹ç›®æ¥æŸ¥çœ‹è¿™äº›ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="46"/>
      <source>Thickness</source>
      <translation>åŽšåº¦</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="75"/>
      <source>Mode</source>
      <translation>æ¨¡å¼</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="83"/>
      <source>Skin</source>
      <translation>è¡¨çš®</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="88"/>
      <source>Pipe</source>
      <translation>ç®¡é“</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="93"/>
      <source>Recto verso</source>
      <translation>æ­£åé¢</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="101"/>
      <source>Join type</source>
      <translation>è¿žæŽ¥ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="109"/>
      <source>Arc</source>
      <translation>åœ†å¼§</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="114"/>
      <location filename="../../TaskThicknessParameters.ui" line="124"/>
      <source>Intersection</source>
      <translation>äº¤é›†</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.ui" line="131"/>
      <source>Make thickness inwards</source>
      <translation>åŽšåº¦æ–¹å‘å‘é‡Œ</translation>
    </message>
    <message>
      <location filename="../../TaskThicknessParameters.cpp" line="269"/>
      <source>Empty thickness created!
</source>
      <translation>å·²åˆ›å»ºç©ºåŽšåº¦ï¼
</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskTransformedParameters</name>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="111"/>
      <source>Remove</source>
      <translation>ç§»é™¤</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="404"/>
      <source>Normal sketch axis</source>
      <translation>æ³•å‘è‰å›¾è½´</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="403"/>
      <source>Vertical sketch axis</source>
      <translation>åž‚ç›´è‰å›¾è½´</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="402"/>
      <source>Horizontal sketch axis</source>
      <translation>æ°´å¹³è‰å›¾è½´</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="406"/>
      <location filename="../../TaskTransformedParameters.cpp" line="442"/>
      <source>Construction line %1</source>
      <translation>è¾…åŠ©çº¿ %1</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="420"/>
      <source>Base X-axis</source>
      <translation>X è½´</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="421"/>
      <source>Base Y-axis</source>
      <translation>Y è½´</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="422"/>
      <source>Base Z-axis</source>
      <translation>Z è½´</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="456"/>
      <source>Base XY-plane</source>
      <translation>åŸºå‡† XY å¹³é¢</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="457"/>
      <source>Base YZ-plane</source>
      <translation>åŸºå‡† YZ å¹³é¢</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="458"/>
      <source>Base XZ-plane</source>
      <translation>åŸºå‡† XZ å¹³é¢</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.cpp" line="430"/>
      <location filename="../../TaskTransformedParameters.cpp" line="466"/>
      <source>Select referenceâ€¦</source>
      <translation>é€‰æ‹©å‚è€ƒâ€¦</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.ui" line="35"/>
      <source>Transform body</source>
      <translation>å˜æ¢å®žä½“</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.ui" line="48"/>
      <source>Transform tool shapes</source>
      <translation>å˜æ¢å·¥å…·å›¾æ ·å½¢çŠ¶</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.ui" line="78"/>
      <source>Add Feature</source>
      <translation>æ·»åŠ ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.ui" line="88"/>
      <source>Remove Feature</source>
      <translation>ç§»é™¤ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.ui" line="122"/>
      <source>Recompute on change</source>
      <translation>æ›´æ”¹æ—¶é‡æ–°è®¡ç®—</translation>
    </message>
    <message>
      <location filename="../../TaskTransformedParameters.ui" line="106"/>
      <source>List can be reordered by dragging</source>
      <translation>åˆ—è¡¨å¯ä»¥é€šè¿‡æ‹–åŠ¨é‡æ–°æŽ’åº</translation>
    </message>
  </context>
  <context>
    <name>PartDesign_MoveFeature</name>
    <message>
      <location filename="../../CommandBody.cpp" line="917"/>
      <source>Select Body</source>
      <translation>é€‰æ‹©å®žä½“</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="918"/>
      <source>Select a body from the list</source>
      <translation>ä»Žåˆ—è¡¨ä¸­é€‰æ‹©å®žä½“</translation>
    </message>
  </context>
  <context>
    <name>PartDesign_MoveFeatureInTree</name>
    <message>
      <location filename="../../CommandBody.cpp" line="1106"/>
      <source>Move Feature Afterâ€¦</source>
      <translation>å‘åŽç§»åŠ¨ç‰¹å¾â€¦</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1107"/>
      <source>Select a feature from the list</source>
      <translation>ä»Žåˆ—è¡¨ä¸­é€‰æ‹©ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1194"/>
      <source>Move Tip</source>
      <translation>ç§»åŠ¨å°–ç«¯</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1200"/>
      <source>Set tip to last feature?</source>
      <translation>å°†å°–ç«¯è®¾ç½®ä¸ºæœ€åŽä¸€ä¸ªç‰¹å¾ï¼Ÿ</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1195"/>
      <source>The moved feature appears after the currently set tip.</source>
      <translation>è¢«ç§»åŠ¨ç‰¹å¾å‡ºçŽ°åœ¨å½“å‰è®¾ç½®çš„ç»“ç®—ä½ç½®ä¹‹åŽã€‚</translation>
    </message>
  </context>
  <context>
    <name>QObject</name>
    <message>
      <location filename="../../Command.cpp" line="149"/>
      <source>Invalid selection</source>
      <translation>æ— æ•ˆé€‰æ‹©</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="150"/>
      <source>There are no attachment modes that fit selected objects. Select something else.</source>
      <translation>æ²¡æœ‰é€‚åˆé€‰å®šå¯¹è±¡çš„é™„ç€æ¨¡å¼ã€‚è¯·é€‰æ‹©å…¶ä»–çš„ä¸œè¥¿ã€‚</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="163"/>
      <location filename="../../Command.cpp" line="171"/>
      <location filename="../../Command.cpp" line="178"/>
      <source>Error</source>
      <translation>é”™è¯¯</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="812"/>
      <source>Several sub-elements selected</source>
      <translation>è‹¥å¹²å­å…ƒç´ è¢«é€‰æ‹©</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="813"/>
      <source>Select a single face as support for a sketch!</source>
      <translation>é€‰æ‹©å•ä¸ªé¢ä½œä¸ºè‰å›¾çš„æ”¯æ’‘ï¼</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="820"/>
      <source>Select a face as support for a sketch!</source>
      <translation>é€‰æ‹©ä¸€ä¸ªé¢ä½œä¸ºè‰å›¾çš„æ”¯æ’‘ï¼</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="827"/>
      <source>Need a planar face as support for a sketch!</source>
      <translation>éœ€è¦ä¸€ä¸ªå¹³é¢ä½œä¸ºè‰å›¾çš„æ”¯æ’‘ï¼</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="834"/>
      <source>Create a plane first or select a face to sketch on</source>
      <translation>é¦–å…ˆåˆ›å»ºä¸€ä¸ªå¹³é¢æˆ–é€‰æ‹©ä¸€ä¸ªé¢è¿›è¡Œè‰å›¾ç»˜åˆ¶</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="819"/>
      <source>No support face selected</source>
      <translation>æœªé€‰ä¸­æ”¯æŒé¢</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="826"/>
      <source>No planar support</source>
      <translation>æ— æ”¯æŒå¹³é¢</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="833"/>
      <source>No valid planes in this document</source>
      <translation>æ–‡æ¡£ä¸­æ— æœ‰æ•ˆå¹³é¢</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="731"/>
      <location filename="../../ViewProviderDatum.cpp" line="259"/>
      <location filename="../../ViewProviderShapeBinder.cpp" line="97"/>
      <location filename="../../ViewProvider.cpp" line="137"/>
      <location filename="../../Command.cpp" line="1142"/>
      <source>A dialog is already open in the task panel</source>
      <translation>ä¸€ä¸ªå¯¹è¯æ¡†å·²åœ¨ä»»åŠ¡é¢æ¿æ‰“å¼€</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="996"/>
      <source>Cannot use this command as there is no solid to subtract from.</source>
      <translation>æ— æ³•ä½¿ç”¨æ­¤å‘½ä»¤ï¼Œå› ä¸ºæ²¡æœ‰å¯ä»¥å‡åŽ»çš„å®žä½“ã€‚</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="999"/>
      <source>Ensure that the body contains a feature before attempting a subtractive command.</source>
      <translation>åœ¨å°è¯•å‡æ–™å‘½ä»¤ä¹‹å‰ç¡®ä¿å®žä½“åŒ…å«ç‰¹å¾ã€‚</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1023"/>
      <source>Cannot use selected object. Selected object must belong to the active body</source>
      <translation>æ— æ³•ä½¿ç”¨æ‰€é€‰å¯¹è±¡ã€‚æ‰€é€‰å¯¹è±¡å¿…é¡»å±žäºŽæ´»åŠ¨å®žä½“</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="164"/>
      <source>There is no active body. Please activate a body before inserting a datum entity.</source>
      <translation>å½“å‰æ²¡æœ‰æ¿€æ´»çš„å®žä½“ã€‚è¯·åœ¨æ’å…¥åŸºå‡†å®žä½“ä¹‹å‰æ¿€æ´»ä¸€ä¸ªå®žä½“ã€‚</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="470"/>
      <source>Sub-shape binder</source>
      <translation>å­å½¢çŠ¶ç»‘å®šå™¨</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1055"/>
      <source>No sketch to work on</source>
      <translation>æ²¡æœ‰å¯å·¥ä½œçš„è‰å›¾</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1056"/>
      <source>No sketch is available in the document</source>
      <translation>æ–‡æ¡£æ— å¯ç”¨è‰å›¾</translation>
    </message>
    <message>
      <location filename="../../SketchWorkflow.cpp" line="732"/>
      <location filename="../../ViewProviderDatum.cpp" line="260"/>
      <location filename="../../ViewProviderShapeBinder.cpp" line="98"/>
      <location filename="../../ViewProvider.cpp" line="138"/>
      <location filename="../../Command.cpp" line="1143"/>
      <source>Close this dialog?</source>
      <translation>å…³é—­æ­¤å¯¹è¯æ¡†ï¼Ÿ</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1825"/>
      <location filename="../../Command.cpp" line="1860"/>
      <source>Wrong selection</source>
      <translation>é€‰æ‹©é”™è¯¯</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1826"/>
      <source>Select an edge, face, or body from a single body.</source>
      <translation>ä»Žä¸€å•ä¸€å®žä½“ä¸­é€‰æ‹©ä¸€è¾¹ï¼Œé¢æˆ–ä½“</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1833"/>
      <location filename="../../Command.cpp" line="2195"/>
      <source>Selection is not in the active body</source>
      <translation>é€‰æ‹©ä¸åœ¨æ´»åŠ¨å®žä½“ä¸­</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1861"/>
      <source>Shape of the selected part is empty</source>
      <translation>æ‰€é€‰é›¶ä»¶çš„å½¢çŠ¶ä¸ºç©º</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1834"/>
      <source>Select an edge, face, or body from an active body.</source>
      <translation>ä»Žæ´»åŠ¨å®žä½“ä¸­é€‰æ‹©è¾¹ã€é¢æˆ–ä½“ã€‚</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1026"/>
      <source>Consider using a shape binder or a base feature to reference external geometry in a body</source>
      <translation>è€ƒè™‘ä½¿ç”¨å½¢çŠ¶ç»‘å®šå™¨æˆ–åŸºå‡†ç‰¹å¾åœ¨å®žä½“ä¸­å¼•ç”¨å¤–éƒ¨å‡ ä½•ä½“</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1847"/>
      <source>Wrong object type</source>
      <translation>é”™è¯¯çš„å¯¹è±¡ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="1848"/>
      <source>%1 works only on parts.</source>
      <translation>%1 ä»…èƒ½è¿ä½œäºŽé›¶ä»¶ä¸Šã€‚</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2196"/>
      <source>Please select only one feature in an active body.</source>
      <translation>è¯·åœ¨ä¸€ä¸ªæ´»åŠ¨çš„å®žä½“ä¸­ä»…é€‰æ‹©ä¸€ä¸ªç‰¹å¾ã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="73"/>
      <source>Part creation failed</source>
      <translation>é›¶ä»¶åˆ›å»ºå¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="74"/>
      <source>Failed to create a part object.</source>
      <translation>åˆ›å»ºé›¶ä»¶å¯¹è±¡å¤±è´¥ã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="127"/>
      <location filename="../../CommandBody.cpp" line="135"/>
      <location filename="../../CommandBody.cpp" line="151"/>
      <location filename="../../CommandBody.cpp" line="217"/>
      <source>Bad base feature</source>
      <translation>ä¸æ­£ç¡®çš„åŸºç¡€ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="128"/>
      <source>A body cannot be based on a Part Design feature.</source>
      <translation>å®žä½“ä¸èƒ½åŸºäºŽé›¶ä»¶è®¾è®¡ç‰¹å¾ã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="136"/>
      <source>%1 already belongs to a body and cannot be used as a base feature for another body.</source>
      <translation>%1 å·²ç»å±žäºŽä¸€ä¸ªå®žä½“ï¼Œä¸èƒ½ç”¨ä½œå¦ä¸€ä¸ªå®žä½“çš„åŸºå‡†ç‰¹å¾ã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="152"/>
      <source>Base feature (%1) belongs to other part.</source>
      <translation>åŸºç¡€ç‰¹å¾ (%1) å½•å±žäºŽå…¶ä»–éƒ¨ä»¶ã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="179"/>
      <source>The selected shape consists of multiple solids.
This may lead to unexpected results.</source>
      <translation>æ‰€é€‰å½¢çŠ¶ç”±å¤šä¸ªå®žä½“ç»„æˆã€‚
è¿™å¯èƒ½ä¼šå¯¼è‡´æ„å¤–çš„ç»“æžœã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="185"/>
      <source>The selected shape consists of multiple shells.
This may lead to unexpected results.</source>
      <translation>æ‰€é€‰å½¢çŠ¶ç”±å¤šä¸ªå£³ä½“ç»„æˆã€‚
è¿™å¯èƒ½ä¼šå¯¼è‡´æ„å¤–çš„ç»“æžœã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="191"/>
      <source>The selected shape consists of only a shell.
This may lead to unexpected results.</source>
      <translation>æ‰€é€‰å½¢çŠ¶ä»…ç”±ä¸€ä¸ªå£³ä½“ç»„æˆã€‚
è¿™å¯èƒ½ä¼šå¯¼è‡´æ„å¤–çš„ç»“æžœã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="197"/>
      <source>The selected shape consists of multiple solids or shells.
This may lead to unexpected results.</source>
      <translation>æ‰€é€‰å½¢çŠ¶ç”±å¤šä¸ªå®žä½“æˆ–å£³ä½“ç»„æˆã€‚
è¿™å¯èƒ½ä¼šå¯¼è‡´æ„å¤–çš„ç»“æžœã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="206"/>
      <source>Base feature</source>
      <translation>åŸºç¡€ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="218"/>
      <source>Body may be based on no more than one feature.</source>
      <translation>å®žä½“åŸºäºŽçš„ç‰¹å¾ä¸èƒ½è¶…è¿‡ä¸€ä¸ªã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="233"/>
      <source>Body</source>
      <translation>Body</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="428"/>
      <source>Nothing to migrate</source>
      <translation>æ²¡æœ‰å¯è¿ç§»çš„å¯¹è±¡</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="697"/>
      <source>Select exactly one Part Design feature or a body.</source>
      <translation>è¯·å‡†ç¡®é€‰æ‹©ä¸€ä¸ªé›¶ä»¶è®¾è®¡ç‰¹å¾æˆ–ä¸€ä¸ªå®žä½“ã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="705"/>
      <source>Could not determine a body for the selected feature '%s'.</source>
      <translation>æ— æ³•ç¡®å®šæ‰€é€‰ç‰¹å¾ '%s' çš„å®žä½“ã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="886"/>
      <source>Only features of a single source body can be moved</source>
      <translation>åªèƒ½ç§»åŠ¨å•ä¸€æºå®žä½“çš„ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="621"/>
      <source>Sketch plane cannot be migrated</source>
      <translation>è‰å›¾å¹³é¢ä¸èƒ½è¢«ç§»åŠ¨</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="429"/>
      <source>No Part Design features without body found Nothing to migrate.</source>
      <translation>æœªæ‰¾åˆ°æ²¡æœ‰å®žä½“çš„é›¶ä»¶è®¾è®¡ç‰¹å¾ï¼Œæ— éœ€è¿ç§»ã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="622"/>
      <source>Please edit '%1' and redefine it to use a Base or Datum plane as the sketch plane.</source>
      <translation>è¯·ç¼–è¾‘ '%1'å¹¶ä½¿ç”¨åŸºé¢æˆ–åŸºå‡†å¹³é¢ä½œä¸ºè‰ç»˜å¹³é¢æ¥é‡æ–°å®šä¹‰å®ƒã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="696"/>
      <location filename="../../CommandBody.cpp" line="704"/>
      <location filename="../../CommandBody.cpp" line="718"/>
      <location filename="../../CommandBody.cpp" line="1072"/>
      <location filename="../../CommandBody.cpp" line="1082"/>
      <source>Selection error</source>
      <translation>é€‰æ‹©é”™è¯¯</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="719"/>
      <source>Only a solid feature can be the tip of a body.</source>
      <translation>åªæœ‰å®žä½“ç‰¹å¾æ‰èƒ½æˆä¸ºå®žä½“çš„ç»“ç®—ç‰¹å¾ã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="855"/>
      <location filename="../../CommandBody.cpp" line="885"/>
      <location filename="../../CommandBody.cpp" line="903"/>
      <source>Features cannot be moved</source>
      <translation>ç‰¹å¾æ— æ³•è¢«ç§»åŠ¨</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="856"/>
      <source>Some of the selected features have dependencies in the source body</source>
      <translation>ä¸€äº›é€‰å®šçš„ç‰¹å¾ä¾èµ–äºŽæºå®žä½“</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="904"/>
      <source>There are no other bodies to move to</source>
      <translation>æ²¡æœ‰å…¶ä»–å®žä½“å¯ä»¥ç§»åŠ¨</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1073"/>
      <source>Impossible to move the base feature of a body.</source>
      <translation>æ— æ³•ç§»åŠ¨å®žä½“çš„åŸºç¡€ç‰¹å¾ã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1083"/>
      <source>Select one or more features from the same body.</source>
      <translation>ä»ŽåŒä¸€å®žä½“ä¸Šé€‰æ‹©ä¸€ä¸ªæˆ–å¤šä¸ªç‰¹å¾ã€‚</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1098"/>
      <source>Beginning of the body</source>
      <translation>å®žä½“çš„èµ·å§‹</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1179"/>
      <source>Dependency violation</source>
      <translation>ä¾èµ–å†²çª</translation>
    </message>
    <message>
      <location filename="../../CommandBody.cpp" line="1180"/>
      <source>Early feature must not depend on later feature.

</source>
      <translation>è¾ƒæ—©çš„ç‰¹å¾ä¸èƒ½ä¾èµ–äºŽè¾ƒåŽçš„ç‰¹å¾ã€‚

</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="309"/>
      <source>No previous feature found</source>
      <translation>æœªæ‰¾åˆ°ä¹‹å‰çš„ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="310"/>
      <source>It is not possible to create a subtractive feature without a base feature available</source>
      <translation>å¦‚æžœæ²¡æœ‰å¯ç”¨çš„åŸºç¡€ç‰¹å¾, å°±ä¸å¯èƒ½åˆ›å»ºå‡æ–™ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.cpp" line="208"/>
      <location filename="../../TaskTransformedParameters.cpp" line="439"/>
      <source>Vertical sketch axis</source>
      <translation>åž‚ç›´è‰ç»˜è½´</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.cpp" line="209"/>
      <location filename="../../TaskTransformedParameters.cpp" line="440"/>
      <source>Horizontal sketch axis</source>
      <translation>æ°´å¹³è‰ç»˜è½´</translation>
    </message>
    <message>
      <location filename="../../TaskRevolutionParameters.cpp" line="211"/>
      <source>Construction line %1</source>
      <translation>è¾…åŠ©çº¿ %1</translation>
    </message>
    <message>
      <location filename="../../TaskSketchBasedParameters.cpp" line="96"/>
      <source>Face</source>
      <translation>é¢</translation>
    </message>
    <message>
      <location filename="../../Utils.cpp" line="208"/>
      <source>Active Body Required</source>
      <translation>éœ€è¦æ¿€æ´»çŠ¶æ€çš„å®žä½“</translation>
    </message>
    <message>
      <location filename="../../Utils.cpp" line="150"/>
      <source>To use Part Design, an active body is required in the document. Activate a body (double-click) or create a new one.

For legacy documents with Part Design objects lacking a body, use the migrate function in Part Design to place them into a body.</source>
      <translation>è¦ä½¿ç”¨é›¶ä»¶è®¾è®¡ï¼Œæ–‡æ¡£ä¸­éœ€è¦æœ‰ä¸€ä¸ªæ¿€æ´»çš„å®žä½“ã€‚æ¿€æ´»ä¸€ä¸ªå®žä½“ï¼ˆåŒå‡»ï¼‰æˆ–åˆ›å»ºä¸€ä¸ªæ–°å®žä½“ã€‚

å¯¹äºŽç¼ºå°‘å®žä½“çš„é›¶ä»¶è®¾è®¡å¯¹è±¡çš„æ—§ç‰ˆæ–‡æ¡£ï¼Œè¯·ä½¿ç”¨é›¶ä»¶è®¾è®¡ä¸­çš„è¿ç§»åŠŸèƒ½å°†å®ƒä»¬æ”¾å…¥å®žä½“ä¸­ã€‚</translation>
    </message>
    <message>
      <location filename="../../Utils.cpp" line="209"/>
      <source>To create a new Part Design object, an active body is required in the document. Activate an existing body (double-click) or create a new one.</source>
      <translation>è¦åˆ›å»ºæ–°çš„é›¶ä»¶è®¾è®¡å¯¹è±¡ï¼Œæ–‡æ¡£ä¸­éœ€è¦æœ‰ä¸€ä¸ªæ¿€æ´»çš„å®žä½“ã€‚æ¿€æ´»ä¸€ä¸ªçŽ°æœ‰å®žä½“ï¼ˆåŒå‡»ï¼‰æˆ–åˆ›å»ºä¸€ä¸ªæ–°å®žä½“ã€‚</translation>
    </message>
    <message>
      <location filename="../../Utils.cpp" line="275"/>
      <source>Feature is not in a body</source>
      <translation>ç‰¹å¾ä¸åœ¨å®žä½“å†…</translation>
    </message>
    <message>
      <location filename="../../Utils.cpp" line="276"/>
      <source>In order to use this feature it needs to belong to a body object in the document.</source>
      <translation>è¦ä½¿ç”¨æ­¤ç‰¹å¾, å®ƒéœ€éš¶å±žäºŽæ–‡æ¡£ä¸­çš„å®žä½“å¯¹è±¡ã€‚</translation>
    </message>
    <message>
      <location filename="../../Utils.cpp" line="322"/>
      <source>Feature is not in a part</source>
      <translation>ç‰¹å¾ä¸åœ¨é›¶ä»¶å†…</translation>
    </message>
    <message>
      <location filename="../../Utils.cpp" line="323"/>
      <source>In order to use this feature it needs to belong to a part object in the document.</source>
      <translation>è¦ä½¿ç”¨æ­¤ç‰¹å¾, å®ƒéœ€éš¶å±žäºŽæ–‡æ¡£ä¸­çš„é›¶ä»¶å¯¹è±¡ã€‚</translation>
    </message>
    <message>
      <location filename="../../ViewProviderTransformed.cpp" line="65"/>
      <location filename="../../ViewProviderShapeBinder.cpp" line="227"/>
      <location filename="../../ViewProviderDressUp.cpp" line="64"/>
      <location filename="../../ViewProvider.cpp" line="94"/>
      <source>Edit %1</source>
      <translation>ç¼–è¾‘ %1</translation>
    </message>
    <message>
      <location filename="../../ViewProvider.cpp" line="107"/>
      <source>Set Face Colors</source>
      <translation>è®¾ç½®é¢é¢œè‰²</translation>
    </message>
    <message>
      <location filename="../../ViewProviderDatum.cpp" line="114"/>
      <location filename="../../ViewProviderDatum.cpp" line="214"/>
      <source>Plane</source>
      <translation>å¹³é¢</translation>
    </message>
    <message>
      <location filename="../../ViewProviderDatum.cpp" line="119"/>
      <location filename="../../ViewProviderDatum.cpp" line="209"/>
      <source>Line</source>
      <translation>çº¿</translation>
    </message>
    <message>
      <location filename="../../ViewProviderDatum.cpp" line="124"/>
      <location filename="../../ViewProviderDatum.cpp" line="219"/>
      <source>Point</source>
      <translation>ç‚¹</translation>
    </message>
    <message>
      <location filename="../../ViewProviderDatum.cpp" line="129"/>
      <source>Coordinate System</source>
      <translation>åæ ‡ç³»</translation>
    </message>
    <message>
      <location filename="../../ViewProviderDatum.cpp" line="236"/>
      <source>Edit Datum</source>
      <translation>ç¼–è¾‘åŸºå‡†</translation>
    </message>
    <message>
      <location filename="../../ViewProviderDressUp.cpp" line="93"/>
      <source>Feature error</source>
      <translation>ç‰¹å¾é”™è¯¯</translation>
    </message>
    <message>
      <location filename="../../ViewProviderDressUp.cpp" line="94"/>
      <source>%1 misses a base feature.
This feature is broken and cannot be edited.</source>
      <translation>%1 ç¼ºå°‘åŸºå‡†ç‰¹å¾ã€‚
æ­¤ç‰¹å¾å·²æŸåï¼Œæ— æ³•ç¼–è¾‘ã€‚</translation>
    </message>
    <message>
      <location filename="../../ViewProviderShapeBinder.cpp" line="222"/>
      <source>Edit Shape Binder</source>
      <translation>ç¼–è¾‘å½¢çŠ¶ç»‘å®šå™¨</translation>
    </message>
    <message>
      <location filename="../../ViewProviderShapeBinder.cpp" line="352"/>
      <source>Synchronize</source>
      <translation>åŒæ­¥</translation>
    </message>
    <message>
      <location filename="../../ViewProviderShapeBinder.cpp" line="354"/>
      <source>Select Bound Object</source>
      <translation>é€‰æ‹©ç»‘å®šå¯¹è±¡</translation>
    </message>
    <message>
      <location filename="../../WorkflowManager.cpp" line="156"/>
      <source>The document "%1" you are editing was designed with an old version of Part Design workbench.</source>
      <translation>æ‚¨æ­£åœ¨ç¼–è¾‘çš„æ–‡æ¡£ "%1" æ˜¯ä½¿ç”¨æ—§ç‰ˆæœ¬çš„é›¶ä»¶è®¾è®¡å·¥ä½œå°è®¾è®¡çš„ã€‚</translation>
    </message>
    <message>
      <location filename="../../WorkflowManager.cpp" line="163"/>
      <source>Migrate in order to use modern Part Design features?</source>
      <translation>è¿ç§»ä»¥ä¾¿ä½¿ç”¨çŽ°ä»£é›¶ä»¶è®¾è®¡åŠŸèƒ½ï¼Ÿ</translation>
    </message>
    <message>
      <location filename="../../WorkflowManager.cpp" line="168"/>
      <source>The document "%1" seems to be either in the middle of the migration process from legacy Part Design or have a slightly broken structure.</source>
      <translation>æ–‡æ¡£ "%1" ä¼¼ä¹Žè¦ä¹ˆå¤„äºŽä»Žæ—§ç‰ˆé›¶ä»¶è®¾è®¡è¿ç§»è¿‡ç¨‹çš„ä¸­é—´ï¼Œè¦ä¹ˆå…·æœ‰ç¨å¾®æŸåçš„ç»“æž„ã€‚</translation>
    </message>
    <message>
      <location filename="../../WorkflowManager.cpp" line="175"/>
      <source>Make the migration automatically?</source>
      <translation>è‡ªåŠ¨è¿›è¡Œè¿ç§»å—ï¼Ÿ</translation>
    </message>
    <message>
      <location filename="../../WorkflowManager.cpp" line="178"/>
      <source>Note: If you choose to migrate you won't be able to edit the file with an older AuraCAD version.
If you refuse to migrate you won't be able to use new PartDesign features like Bodies and Parts. As a result you also won't be able to use your parts in the assembly workbench.
Although you will be able to migrate any moment later with 'Part Design -&gt; Migrate'.</source>
      <translation>æ³¨æ„ï¼šå¦‚æžœæ‚¨é€‰æ‹©è¿ç§»ï¼Œæ‚¨å°†æ— æ³•ä½¿ç”¨æ—§ç‰ˆæœ¬çš„ AuraCAD ç¼–è¾‘è¯¥æ–‡ä»¶ã€‚
å¦‚æžœæ‚¨æ‹’ç»è¿ç§»ï¼Œæ‚¨å°†æ— æ³•ä½¿ç”¨æ–°çš„é›¶ä»¶è®¾è®¡åŠŸèƒ½ï¼Œå¦‚å®žä½“å’Œé›¶éƒ¨ä»¶ã€‚å› æ­¤ï¼Œæ‚¨ä¹Ÿå°†æ— æ³•åœ¨è£…é…å·¥ä½œå°ä¸­ä½¿ç”¨æ‚¨çš„é›¶éƒ¨ä»¶ã€‚
å°½ç®¡æ‚¨å¯ä»¥ç¨åŽéšæ—¶ä½¿ç”¨â€œé›¶ä»¶è®¾è®¡ -&gt; è¿ç§»â€è¿›è¡Œè¿ç§»ã€‚</translation>
    </message>
    <message>
      <location filename="../../WorkflowManager.cpp" line="191"/>
      <source>Migrate Manually</source>
      <translation>æ‰‹åŠ¨è¿ç§»</translation>
    </message>
    <message>
      <location filename="../../ViewProviderBoolean.cpp" line="70"/>
      <source>Edit Boolean</source>
      <translation>ç¼–è¾‘å¸ƒå°”è¿ç®—</translation>
    </message>
    <message>
      <location filename="../../ViewProviderChamfer.cpp" line="42"/>
      <source>Edit Chamfer</source>
      <translation>ç¼–è¾‘å€’è§’</translation>
    </message>
    <message>
      <location filename="../../ViewProviderDraft.cpp" line="43"/>
      <source>Edit Draft</source>
      <translation>ç¼–è¾‘æ”¾æ ·</translation>
    </message>
    <message>
      <location filename="../../ViewProviderFillet.cpp" line="42"/>
      <source>Edit Fillet</source>
      <translation>ç¼–è¾‘åœ†è§’</translation>
    </message>
    <message>
      <location filename="../../ViewProviderGroove.cpp" line="45"/>
      <source>Edit Groove</source>
      <translation>ç¼–è¾‘å‡¹æ§½</translation>
    </message>
    <message>
      <location filename="../../ViewProviderHelix.cpp" line="50"/>
      <source>Edit Helix</source>
      <translation>ç¼–è¾‘èžºæ—‹</translation>
    </message>
    <message>
      <location filename="../../ViewProviderHole.cpp" line="129"/>
      <source>Edit Hole</source>
      <translation>ç¼–è¾‘å­”</translation>
    </message>
    <message>
      <location filename="../../ViewProviderLinearPattern.cpp" line="40"/>
      <source>Edit Linear Pattern</source>
      <translation>ç¼–è¾‘çº¿æ€§é˜µåˆ—</translation>
    </message>
    <message>
      <location filename="../../ViewProviderLoft.cpp" line="67"/>
      <source>Edit Loft</source>
      <translation>ç¼–è¾‘æ”¾æ ·</translation>
    </message>
    <message>
      <location filename="../../ViewProviderMirrored.cpp" line="40"/>
      <source>Edit Mirror</source>
      <translation>ç¼–è¾‘é•œåƒ</translation>
    </message>
    <message>
      <location filename="../../ViewProviderMultiTransform.cpp" line="49"/>
      <source>Edit Multi-Transform</source>
      <translation>ç¼–è¾‘å¤šé‡å˜æ¢</translation>
    </message>
    <message>
      <location filename="../../ViewProviderPad.cpp" line="45"/>
      <source>Edit Pad</source>
      <translation>ç¼–è¾‘å‡¸å°</translation>
    </message>
    <message>
      <location filename="../../ViewProviderPipe.cpp" line="77"/>
      <source>Edit Pipe</source>
      <translation>ç¼–è¾‘ç®¡é“</translation>
    </message>
    <message>
      <location filename="../../ViewProviderPocket.cpp" line="47"/>
      <source>Edit Pocket</source>
      <translation>ç¼–è¾‘å£è¢‹</translation>
    </message>
    <message>
      <location filename="../../ViewProviderPolarPattern.cpp" line="40"/>
      <source>Edit Polar Pattern</source>
      <translation>ç¼–è¾‘æžè½´é˜µåˆ—</translation>
    </message>
    <message>
      <location filename="../../ViewProviderPrimitive.cpp" line="52"/>
      <source>Edit Primitive</source>
      <translation>ç¼–è¾‘åŸºå…ƒ</translation>
    </message>
    <message>
      <location filename="../../ViewProviderRevolution.cpp" line="45"/>
      <source>Edit Revolution</source>
      <translation>ç¼–è¾‘æ—‹è½¬ä½“</translation>
    </message>
    <message>
      <location filename="../../ViewProviderScaled.cpp" line="40"/>
      <source>Edit Scale</source>
      <translation>ç¼–è¾‘ç¼©æ”¾</translation>
    </message>
    <message>
      <location filename="../../ViewProviderThickness.cpp" line="42"/>
      <source>Edit Thickness</source>
      <translation>ç¼–è¾‘åŽšåº¦</translation>
    </message>
  </context>
  <context>
    <name>SprocketParameter</name>
    <message>
      <location filename="../../../SprocketFeature.ui" line="14"/>
      <source>Sprocket Parameters</source>
      <translation>é“¾è½®å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="26"/>
      <source>Number of teeth</source>
      <translation>é½¿æ•°</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="52"/>
      <source>Sprocket reference</source>
      <translation>é“¾è½®å‚è€ƒ</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="66"/>
      <source>ANSI 25</source>
      <translation>ANSI 25</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="71"/>
      <source>ANSI 35</source>
      <translation>ANSI 35</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="76"/>
      <source>ANSI 41</source>
      <translation>ANSI 41</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="81"/>
      <source>ANSI 40</source>
      <translation>ANSI 40</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="86"/>
      <source>ANSI 50</source>
      <translation>ANSI 50</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="91"/>
      <source>ANSI 60</source>
      <translation>ANSI 60</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="96"/>
      <source>ANSI 80</source>
      <translation>ANSI 80</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="101"/>
      <source>ANSI 100</source>
      <translation>ANSI 100</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="106"/>
      <source>ANSI 120</source>
      <translation>ANSI 120</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="111"/>
      <source>ANSI 140</source>
      <translation>ANSI 140</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="116"/>
      <source>ANSI 160</source>
      <translation>ANSI 160</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="121"/>
      <source>ANSI 180</source>
      <translation>ANSI 180</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="126"/>
      <source>ANSI 200</source>
      <translation>ANSI 200</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="131"/>
      <source>ANSI 240</source>
      <translation>ANSI 240</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="136"/>
      <source>Bicycle with derailleur</source>
      <translation>å¸¦å˜é€Ÿå™¨çš„è‡ªè¡Œè½¦</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="141"/>
      <source>Bicycle without derailleur</source>
      <translation>ä¸å¸¦å˜é€Ÿå™¨çš„è‡ªè¡Œè½¦</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="219"/>
      <source>Chain pitch</source>
      <translation>é“¾è·</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="266"/>
      <source>Chain roller diameter</source>
      <translation>é“¾è½®ç›´å¾„</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="310"/>
      <source>Tooth width</source>
      <translation>é½¿å®½</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="146"/>
      <source>ISO 606 06B</source>
      <translation>ISO 606 06B</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="151"/>
      <source>ISO 606 08B</source>
      <translation>ISO 606 08B</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="156"/>
      <source>ISO 606 10B</source>
      <translation>ISO 606 10B</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="161"/>
      <source>ISO 606 12B</source>
      <translation>ISO 606 12B</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="166"/>
      <source>ISO 606 16B</source>
      <translation>ISO 606 16B</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="171"/>
      <source>ISO 606 20B</source>
      <translation>ISO 606 20B</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="176"/>
      <source>ISO 606 24B</source>
      <translation>ISO 606 24B</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="181"/>
      <source>Motorcycle 420</source>
      <translation>æ‘©æ‰˜è½¦ 420</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="186"/>
      <source>Motorcycle 425</source>
      <translation>æ‘©æ‰˜è½¦ 425</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="191"/>
      <source>Motorcycle 428</source>
      <translation>æ‘©æ‰˜è½¦ 428</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="196"/>
      <source>Motorcycle 520</source>
      <translation>æ‘©æ‰˜è½¦ 520</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="201"/>
      <source>Motorcycle 525</source>
      <translation>æ‘©æ‰˜è½¦ 525</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="206"/>
      <source>Motorcycle 530</source>
      <translation>æ‘©æ‰˜è½¦ 530</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="211"/>
      <source>Motorcycle 630</source>
      <translation>æ‘©æ‰˜è½¦ 630</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.ui" line="238"/>
      <source>0 in</source>
      <translation>0 åˆ°</translation>
    </message>
  </context>
  <context>
    <name>TaskHoleParameters</name>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="824"/>
      <source>Live update of changes to the thread
Note that the calculation can take some time</source>
      <translation>å®žæ—¶æ›´æ–°å¯¹èžºçº¹çš„æ›´æ”¹
æ³¨æ„è®¡ç®—å¯èƒ½éœ€è¦ä¸€äº›æ—¶é—´</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="1019"/>
      <source>Thread Depth</source>
      <translation>èžºçº¹æ·±åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="1072"/>
      <source>Customize thread clearance</source>
      <translation>è‡ªå®šä¹‰èžºçº¹é—´éš™</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="699"/>
      <source>Clearance</source>
      <translation>é—´éš™</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="65"/>
      <source>Head type</source>
      <translation>å¤´éƒ¨ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="153"/>
      <source>Depth type</source>
      <translation>æ·±åº¦ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="245"/>
      <source>Head diameter</source>
      <translation>å¤´éƒ¨ç›´å¾„</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="293"/>
      <source>Head depth</source>
      <translation>å¤´éƒ¨æ·±åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="668"/>
      <source>Clearance / Passthrough</source>
      <translation>é—´éš™ / é€šè¿‡å­”</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="686"/>
      <source>Hole type</source>
      <translation>å­”ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="828"/>
      <source>Update thread view</source>
      <translation>æ›´æ–°èžºçº¹è§†å›¾</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="1078"/>
      <source>Custom Clearance</source>
      <translation>è‡ªå®šä¹‰é—´éš™</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="1091"/>
      <source>Custom Thread clearance value</source>
      <translation>è‡ªå®šä¹‰èžºçº¹é—´éš™å¤§å°</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="881"/>
      <source>Direction</source>
      <translation>æ–¹å‘</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="49"/>
      <source>Size</source>
      <translation>å¤§å°</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="712"/>
      <source>Hole clearance
Only available for holes without thread</source>
      <translation>å­”ä½
ä»…é€‚ç”¨äºŽæ— èžºçº¹å­”</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="88"/>
      <location filename="../../TaskHoleParameters.ui" line="717"/>
      <source>Standard</source>
      <translation>æ ‡å‡†</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="673"/>
      <source>Tap drill</source>
      <translation>æ”»ä¸é’»å­”</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="678"/>
      <source>Threaded</source>
      <translation>å¸¦èžºçº¹çš„</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="722"/>
      <source>Close</source>
      <translation>å…³é—­</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="727"/>
      <source>Wide</source>
      <translation>å®½åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="805"/>
      <source>Whether the hole gets a modelled thread</source>
      <translation>è¯¥å­”æ˜¯å¦ç”Ÿæˆä¸€ä¸ªå»ºæ¨¡èžºçº¹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="808"/>
      <source>Model Thread</source>
      <translation>å»ºæ¨¡èžºçº¹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="861"/>
      <source>Class</source>
      <translation>ç­‰çº§</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="848"/>
      <source>Tolerance class for threaded holes according to hole profile</source>
      <translation>æ ¹æ®å­”é…ç½®æ–¹æ¡ˆèžºçº¹å­”çš„å…¬å·®ç­‰çº§</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="552"/>
      <source>Diameter</source>
      <translation>ç›´å¾„</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="574"/>
      <source>Hole diameter</source>
      <translation>å­”ç›´å¾„</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="507"/>
      <source>Depth</source>
      <translation>æ·±åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="20"/>
      <source>Hole Parameters</source>
      <translation>å­”å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="95"/>
      <source>Base profile types</source>
      <translation>åŸºæœ¬è½®å»“ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="126"/>
      <source>Circles and arcs</source>
      <translation>åœ†å’Œåœ†å¼§</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="131"/>
      <source>Points, circles and arcs</source>
      <translation>ç‚¹ã€åœ†å’Œåœ†å¼§</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="136"/>
      <source>Points</source>
      <translation>ç‚¹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="170"/>
      <location filename="../../TaskHoleParameters.ui" line="989"/>
      <source>Dimension</source>
      <translation>å°ºå¯¸</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="175"/>
      <source>Through all</source>
      <translation>é€šè¿‡æ‰€æœ‰</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="197"/>
      <source>Custom head values</source>
      <translation>è‡ªå®šä¹‰å¤´éƒ¨å€¼</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="367"/>
      <source>Drill angle</source>
      <extracomment>Translate it as short as possible</extracomment>
      <translation>é’»å­”è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="403"/>
      <source>Include in depth</source>
      <extracomment>Translate it as short as possible</extracomment>
      <translation>åŒ…å«åœ¨æ·±åº¦ä¸­</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="610"/>
      <source>Switch direction</source>
      <translation>åˆ‡æ¢æ–¹å‘</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="773"/>
      <source>Thread</source>
      <translation>èžºçº¹é“£</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="905"/>
      <source>&amp;Right hand</source>
      <translation>å³æ‰‹(&amp;R)</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="921"/>
      <source>&amp;Left hand</source>
      <translation>å·¦æ‰‹(&amp;L)</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="970"/>
      <source>Thread Depth Type</source>
      <translation>èžºçº¹æ·±åº¦ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="984"/>
      <source>Hole depth</source>
      <translation>å­”æ·±åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="994"/>
      <source>Tapped (DIN76)</source>
      <translation>èžºçº¹ (DIN76)</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="118"/>
      <source>Cut type for screw heads</source>
      <translation>èžºä¸å¤´çš„åˆ‡å‰²ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="191"/>
      <source>Check to override the values predefined by the 'Type'</source>
      <translation>æ£€æŸ¥ä»¥è¦†ç›–â€œç±»åž‹â€é¢„å®šä¹‰çš„å€¼</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="306"/>
      <source>For countersinks this is the depth of
the screw's top below the surface</source>
      <translation>å¯¹äºŽæ²‰å¤´å­”ï¼Œè¿™æ˜¯èžºé’‰é¡¶éƒ¨åˆ°æ²‰å¤´è¡¨é¢çš„æ·±åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="462"/>
      <source>Countersink angle</source>
      <translation>åŸ‹å¤´å­”è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="399"/>
      <source>The size of the drill point will be taken into
account for the depth of blind holes</source>
      <translation>é’»å­”ç‚¹çš„å¤§å°å°†è¢«è®¡å…¥
ç›²å­”çš„æ·±åº¦</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="626"/>
      <source>Tapered</source>
      <translation>é”¥å­”</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="639"/>
      <source>Taper angle for the hole
90 degree: straight hole
under 90: smaller hole radius at the bottom
over 90: larger hole radius at the bottom</source>
      <translation>å­”çš„é”¥åº¦ï¼š
90åº¦ï¼šç›´å­”
å°äºŽ90ï¼šåº•éƒ¨çš„è¾ƒå°å­”åŠå¾„
å¤§äºŽ90ï¼šåº•éƒ¨çš„è¾ƒå¤§å­”åŠå¾„</translation>
    </message>
    <message>
      <location filename="../../TaskHoleParameters.ui" line="607"/>
      <source>Reverses the hole direction</source>
      <translation>åè½¬å­”æ–¹å‘</translation>
    </message>
  </context>
  <context>
    <name>TaskTransformedMessages</name>
    <message>
      <location filename="../../TaskTransformedMessages.ui" line="25"/>
      <source>No message</source>
      <translation>æ— æ¶ˆæ¯</translation>
    </message>
  </context>
  <context>
    <name>Workbench</name>
    <message>
      <location filename="../../Workbench.cpp" line="43"/>
      <source>&amp;Sketch</source>
      <translation>è‰å›¾(&amp;S)</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="45"/>
      <source>&amp;Part Design</source>
      <translation>é›¶ä»¶è®¾è®¡(&amp;P)</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="46"/>
      <source>Datums</source>
      <translation>åŸºå‡†</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="47"/>
      <source>Additive Features</source>
      <translation>å¢žæ–™ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="48"/>
      <source>Subtractive Features</source>
      <translation>å‡æ–™ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="49"/>
      <source>Dress-Up Features</source>
      <translation>ä¿®æ•´ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="50"/>
      <source>Transformation Features</source>
      <translation>å˜æ¢ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="51"/>
      <source>Sprocketâ€¦</source>
      <translation>é“¾è½®â€¦</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="52"/>
      <source>Involute Gear</source>
      <translation>æ¸å¼€çº¿é½¿è½®</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="54"/>
      <source>Shaft Design Wizard</source>
      <translation>è½´è®¾è®¡å‘å¯¼</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="62"/>
      <source>Measure</source>
      <translation>æµ‹é‡</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="63"/>
      <source>Refresh</source>
      <translation>åˆ·æ–°</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="64"/>
      <source>Toggle 3D</source>
      <translation>åˆ‡æ¢3D</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="65"/>
      <source>Part Design Helper</source>
      <translation>é›¶ä»¶è®¾è®¡åŠ©æ‰‹</translation>
    </message>
    <message>
      <location filename="../../Workbench.cpp" line="66"/>
      <source>Part Design Modeling</source>
      <translation>é›¶ä»¶è®¾è®¡å»ºæ¨¡</translation>
    </message>
  </context>
  <context>
    <name>WizardShaftTable</name>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="48"/>
      <source>Length [mm]</source>
      <translation>é•¿åº¦ [mm]</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="49"/>
      <source>Diameter [mm]</source>
      <translation>ç›´å¾„ [mm]</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="50"/>
      <source>Inner diameter [mm]</source>
      <translation>å†…ç›´å¾„ [mm]</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="51"/>
      <source>Constraint type</source>
      <translation>çº¦æŸç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="52"/>
      <source>Start edge type</source>
      <translation>èµ·å§‹è¾¹ç¼˜ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="53"/>
      <source>Start edge size</source>
      <translation>èµ·å§‹è¾¹ç¼˜å°ºå¯¸</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="54"/>
      <source>End edge type</source>
      <translation>ç»“æŸè¾¹ç¼˜ç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="55"/>
      <source>End edge size</source>
      <translation>ç»“æŸè¾¹ç¼˜å¤§å°</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="69"/>
      <source>Shaft Wizard</source>
      <translation>è½´å‘å¯¼å‘</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="77"/>
      <source>Section 1</source>
      <translation>æˆªé¢1</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="78"/>
      <source>Section 2</source>
      <translation>æˆªé¢2</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="82"/>
      <source>Add column</source>
      <translation>æ·»åŠ åˆ—</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="130"/>
      <source>Section %s</source>
      <translation>æˆªé¢ %s</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="159"/>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="178"/>
      <source>None</source>
      <translation>æ— </translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="160"/>
      <source>Fixed</source>
      <translation>å›ºå®š</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="161"/>
      <source>Force</source>
      <translation>åŠ›</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="162"/>
      <source>Bearing</source>
      <translation>è½´æ‰¿</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="163"/>
      <source>Gear</source>
      <translation>é½¿è½®</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="164"/>
      <source>Pulley</source>
      <translation>æ»‘è½®</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="181"/>
      <source>Chamfer</source>
      <translation>å€’è§’</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaftTable.py" line="182"/>
      <source>Fillet</source>
      <translation>åœ†è§’</translation>
    </message>
  </context>
  <context>
    <name>TaskWizardShaft</name>
    <message>
      <location filename="../../../WizardShaft/WizardShaft.py" line="60"/>
      <source>All</source>
      <translation>å…¨éƒ¨</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaft.py" line="120"/>
      <source>Missing Module</source>
      <translation>ç¼ºå°‘æ¨¡å—</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaft.py" line="126"/>
      <source>The Plot add-on is not installed. Install it to enable this feature.</source>
      <translation>æœªå®‰è£…ç»˜å›¾é™„åŠ ç»„ä»¶ã€‚è¯·å®‰è£…å®ƒä»¥å¯ç”¨æ­¤åŠŸèƒ½ã€‚</translation>
    </message>
  </context>
  <context>
    <name>PartDesign_WizardShaftCallBack</name>
    <message>
      <location filename="../../../WizardShaft/WizardShaft.py" line="253"/>
      <source>Shaft design wizard...</source>
      <translation>è½´è®¾è®¡å‘å¯¼...</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaft.py" line="256"/>
      <source>Start the shaft design wizard</source>
      <translation>å¯åŠ¨è½´è®¾è®¡å‘å¯¼</translation>
    </message>
  </context>
  <context>
    <name>Exception</name>
    <message>
      <location filename="../../../App/Body.cpp" line="405"/>
      <source>Linked object is not a PartDesign feature</source>
      <translation>é“¾æŽ¥å¯¹è±¡ä¸æ˜¯ PartDesign åŠŸèƒ½</translation>
    </message>
    <message>
      <location filename="../../../App/Body.cpp" line="414"/>
      <source>Tip shape is empty</source>
      <translation>æç¤ºå½¢çŠ¶ä¸ºç©º</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureBase.cpp" line="68"/>
      <source>BaseFeature link is not set</source>
      <translation>åŸºç¡€ç‰¹å¾é“¾æŽ¥æœªè®¾ç½®</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureBase.cpp" line="74"/>
      <source>BaseFeature must be a Part::Feature</source>
      <translation>åŸºç¡€ç‰¹å¾å¿…é¡»æ˜¯ Part::Feature</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureBase.cpp" line="84"/>
      <source>BaseFeature has an empty shape</source>
      <translation>åŸºç¡€ç‰¹å¾æœ‰ç©ºå½¢çŠ¶</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureBoolean.cpp" line="77"/>
      <source>Cannot do boolean cut without BaseFeature</source>
      <translation>æ— åŸºç¡€ç‰¹å¾æ—¶æ— æ³•è¿›è¡Œå¸ƒå°”å‰ªåˆ‡</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureBoolean.cpp" line="94"/>
      <source>Cannot do boolean with anything but Part::Feature and its derivatives</source>
      <translation>é™¤ Part::Feature åŠå…¶è¡ç”Ÿå¤–ï¼Œæ— æ³•è¿›è¡Œå¸ƒå°”æ“ä½œ</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureBoolean.cpp" line="106"/>
      <source>Cannot do boolean operation with invalid base shape</source>
      <translation>æ— æ³•å¯¹æ— æ•ˆçš„åŸºç¡€å½¢çŠ¶è¿›è¡Œå¸ƒå°”æ“ä½œ</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureLoft.cpp" line="333"/>
      <location filename="../../../App/FeatureLoft.cpp" line="377"/>
      <location filename="../../../App/FeatureDraft.cpp" line="335"/>
      <location filename="../../../App/FeatureFillet.cpp" line="142"/>
      <location filename="../../../App/FeatureRevolved.cpp" line="217"/>
      <location filename="../../../App/FeatureExtrude.cpp" line="775"/>
      <location filename="../../../App/FeatureExtrude.cpp" line="791"/>
      <location filename="../../../App/FeatureExtrude.cpp" line="804"/>
      <location filename="../../../App/FeaturePipe.cpp" line="482"/>
      <location filename="../../../App/FeaturePipe.cpp" line="531"/>
      <location filename="../../../App/FeatureBoolean.cpp" line="161"/>
      <location filename="../../../App/FeatureChamfer.cpp" line="196"/>
      <location filename="../../../App/FeatureHole.cpp" line="2101"/>
      <source>Result has multiple solids: enable 'Allow Compound' in the active body.</source>
      <translation>ç»“æžœæœ‰å¤šä¸ªå®žä½“ï¼šåœ¨æ´»åŠ¨å®žä½“ä¸­å¯ç”¨â€œå…è®¸å¤åˆâ€</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureBoolean.cpp" line="116"/>
      <source>Tool shape is null</source>
      <translation>å·¥å…·å½¢çŠ¶ä¸ºç©º</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureBoolean.cpp" line="143"/>
      <source>Unsupported boolean operation</source>
      <translation>ä¸æ”¯æŒçš„å¸ƒå°”æ“ä½œ</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureExtrude.cpp" line="353"/>
      <source>Cannot create a pad with a total length of zero.</source>
      <translation>æ— æ³•åˆ›å»ºæ€»é•¿åº¦ä¸ºé›¶çš„åž«ç‰‡ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureExtrude.cpp" line="358"/>
      <source>Cannot create a pocket with a total length of zero.</source>
      <translation>æ— æ³•åˆ›å»ºæ€»é•¿åº¦ä¸ºé›¶çš„å£è¢‹ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureExtrude.cpp" line="706"/>
      <source>No extrusion geometry was generated.</source>
      <translation>æœªç”Ÿæˆä»»ä½•æ‹‰ä¼¸å‡ ä½•ä½“ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureExtrude.cpp" line="730"/>
      <source>Resulting fused extrusion is null.</source>
      <translation>ç»“æžœèžåˆçš„æ‹‰ä¼¸ä¸º nullã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureLoft.cpp" line="370"/>
      <location filename="../../../App/FeatureExtrude.cpp" line="766"/>
      <location filename="../../../App/FeaturePipe.cpp" line="523"/>
      <location filename="../../../App/FeaturePrimitive.cpp" line="141"/>
      <source>Resulting shape is not a solid</source>
      <translation>ç»“æžœå½¢çŠ¶ä¸æ˜¯å®žä½“</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureChamfer.cpp" line="176"/>
      <source>Failed to create chamfer</source>
      <translation>åˆ›å»ºå€’è§’å¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureDraft.cpp" line="330"/>
      <location filename="../../../App/FeatureFillet.cpp" line="122"/>
      <source>Resulting shape is null</source>
      <translation>ç»“æžœå½¢çŠ¶ä¸ºç©º</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureChamfer.cpp" line="144"/>
      <source>No edges specified</source>
      <translation>æœªæŒ‡å®šè¾¹</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureChamfer.cpp" line="211"/>
      <source>Chamfer failed: OCC kernel error in chamfer computation</source>
      <translation>å€’è§’å¤±è´¥ï¼šOCC å†…æ ¸åœ¨å€’è§’è®¡ç®—ä¸­å‘ç”Ÿé”™è¯¯</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureChamfer.cpp" line="302"/>
      <source>Size must be greater than zero</source>
      <translation>å°ºå¯¸å¿…é¡»å¤§äºŽ 0</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureChamfer.cpp" line="313"/>
      <source>Size2 must be greater than zero</source>
      <translation>å°ºå¯¸2 å¿…é¡»å¤§äºŽ 0</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureChamfer.cpp" line="320"/>
      <source>Angle must be greater than 0 and less than 180</source>
      <translation>è§’åº¦å¿…é¡»å¤§äºŽ 0 ä¸”å°äºŽ 180 åº¦</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureFillet.cpp" line="97"/>
      <source>Fillet not possible on selected shapes</source>
      <translation>é€‰æ‹©çš„å½¢çŠ¶ä¸Šæ— æ³•è¿›è¡Œåœ†è§’å¤„ç†</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureFillet.cpp" line="105"/>
      <source>Fillet radius must be greater than zero</source>
      <translation>åœ†è§’åŠå¾„å¿…é¡»å¤§äºŽ 0</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureFillet.cpp" line="159"/>
      <source>Fillet operation failed. The selected edges may contain geometry that cannot be filleted together. Try filleting edges individually or with a smaller radius.</source>
      <translation>åœ†è§’æ“ä½œå¤±è´¥ã€‚é€‰å®šçš„è¾¹å¯èƒ½åŒ…å«æ— æ³•åŒæ—¶è¿›è¡Œåœ†è§’å¤„ç†çš„å‡ ä½•å›¾å½¢ã€‚è¯·å°è¯•å•ç‹¬å¯¹è¾¹è¿›è¡Œåœ†è§’å¤„ç†ï¼Œæˆ–ä½¿ç”¨æ›´å°çš„åœ†è§’åŠå¾„ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1739"/>
      <source>The requested feature cannot be created. The reason may be that:
  - the active Body does not contain a base shape, so there is no
  material to be removed;
  - the selected sketch does not belong to the active Body.</source>
      <translation>æ— æ³•åˆ›å»ºè¯·æ±‚çš„åŠŸèƒ½ã€‚ åŽŸå› å¯èƒ½æ˜¯ï¼š
  - æ´»åŠ¨å®žä½“ä¸åŒ…å«åŸºç¡€å½¢çŠ¶ï¼Œ å› æ­¤æ²¡æœ‰
  ææ–™å¯è¢«åˆ é™¤ï¼›
  - é€‰ä¸­çš„è‰å›¾ä¸å±žäºŽæ´»åŠ¨å®žä½“ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureExtrude.cpp" line="402"/>
      <source>Failed to obtain profile shape</source>
      <translation>æ— æ³•èŽ·å–è½®å»“å½¢çŠ¶</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureExtrude.cpp" line="456"/>
      <source>Creation failed because direction is orthogonal to sketch's normal vector</source>
      <translation>åˆ›å»ºå¤±è´¥ï¼Œæ–¹å‘ä¸Žè‰å›¾çš„æ³•çº¿çŸ¢é‡æ­£äº¤</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureRevolved.cpp" line="132"/>
      <location filename="../../../App/FeatureExtrude.cpp" line="479"/>
      <source>Creating a face from sketch failed</source>
      <translation>ä»Žè‰å›¾åˆ›å»ºé¢å¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureRevolved.cpp" line="152"/>
      <source>Revolve axis intersects the sketch</source>
      <translation>æ—‹è½¬è½´ä¸Žè‰å›¾ç›¸äº¤</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureRevolved.cpp" line="202"/>
      <source>Could not revolve the sketch!</source>
      <translation>æ— æ³•æ—‹è½¬è‰å›¾ï¼</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureRevolved.cpp" line="69"/>
      <source>Could not create face from sketch.
Intersecting sketch entities in a sketch are not allowed.</source>
      <translation>æ— æ³•ä»Žè‰å›¾ä¸­åˆ›å»ºé¢ã€‚
ä¸å…è®¸åœ¨è‰å›¾ä¸­äº¤å‰å®žä½“ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="237"/>
      <source>Error: Pitch too small!</source>
      <translation>é”™è¯¯ï¼šèŠ‚è·å¤ªå°ï¼</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="242"/>
      <location filename="../../../App/FeatureHelix.cpp" line="265"/>
      <source>Error: height too small!</source>
      <translation>é”™è¯¯ï¼šé«˜åº¦å¤ªå°ï¼</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="251"/>
      <source>Error: pitch too small!</source>
      <translation>é”™è¯¯ï¼šèŠ‚è·å¤ªå°ï¼</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="256"/>
      <location filename="../../../App/FeatureHelix.cpp" line="270"/>
      <location filename="../../../App/FeatureHelix.cpp" line="279"/>
      <source>Error: turns too small!</source>
      <translation>é”™è¯¯ï¼šåœˆæ•°å¤ªå°ï¼</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="285"/>
      <source>Error: either height or growth must not be zero!</source>
      <translation>é”™è¯¯ï¼šé«˜åº¦å’Œå¢žé•¿çŽ‡ä¸èƒ½ä¸ºé›¶ï¼</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="303"/>
      <source>Error: unsupported mode</source>
      <translation>é”™è¯¯ï¼šä¸æ”¯æŒçš„æ¨¡å¼</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="317"/>
      <source>Error: No valid sketch or face</source>
      <translation>é”™è¯¯ï¼šæ²¡æœ‰æœ‰æ•ˆçš„è‰å›¾æˆ–é¢</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="330"/>
      <source>Error: Face must be planar</source>
      <translation>é”™è¯¯ï¼šé¢å¿…é¡»æ˜¯å¹³é¢</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="445"/>
      <location filename="../../../App/FeatureHelix.cpp" line="486"/>
      <location filename="../../../App/FeatureHole.cpp" line="2457"/>
      <source>Error: Result is not a solid</source>
      <translation>é”™è¯¯ï¼šç»“æžœä¸æ˜¯å®žä½“</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="415"/>
      <source>Error: There is nothing to subtract</source>
      <translation>é”™è¯¯: æ²¡æœ‰å¯å‡å°‘çš„å†…å®¹</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="421"/>
      <location filename="../../../App/FeatureHelix.cpp" line="451"/>
      <location filename="../../../App/FeatureHelix.cpp" line="492"/>
      <source>Error: Result has multiple solids</source>
      <translation>é”™è¯¯ï¼šç»“æžœæœ‰å¤šä¸ªå®žä½“</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="436"/>
      <source>Error: Adding the helix failed</source>
      <translation>é”™è¯¯ï¼šæ·»åŠ èžºæ—‹å¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="468"/>
      <source>Error: Intersecting the helix failed</source>
      <translation>é”™è¯¯ï¼šäº¤å‰èžºæ—‹å¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="477"/>
      <source>Error: Subtracting the helix failed</source>
      <translation>é”™è¯¯ï¼šå‡åŽ»èžºæ—‹å¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHelix.cpp" line="508"/>
      <source>Error: Could not create face from sketch</source>
      <translation>é”™è¯¯ï¼šæ— æ³•ä»Žè‰å›¾åˆ›å»ºé¢</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1233"/>
      <source>Thread type is invalid</source>
      <translation>èžºçº¹ç±»åž‹æ— æ•ˆ</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1752"/>
      <source>Hole error: Diameter too small</source>
      <translation>å­”å¾„é”™è¯¯ï¼šç›´å¾„è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1789"/>
      <source>Hole error: Unsupported length specification</source>
      <translation>å­”é”™è¯¯ï¼šä¸æ”¯æŒçš„é•¿åº¦</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1795"/>
      <source>Hole error: Invalid hole depth</source>
      <translation>å­”é”™è¯¯ï¼šæ— æ•ˆçš„å­”æ·±åº¦</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1821"/>
      <source>Hole error: Invalid taper angle</source>
      <translation>å­”é”™è¯¯ï¼šæ— æ•ˆæ–œè§’</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1845"/>
      <source>Hole error: Hole cut diameter too small</source>
      <translation>å­”é”™è¯¯ï¼šæŒ–å­”ç›´å¾„å¤ªå°</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1850"/>
      <source>Hole error: Hole cut depth must be less than hole depth</source>
      <translation>å­”é”™è¯¯ï¼šå­”åˆ‡å‰²æ·±åº¦å¿…é¡»å°äºŽå­”æ·±åº¦</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1857"/>
      <source>Hole error: Hole cut depth must be greater or equal to zero</source>
      <translation>å­”é”™è¯¯ï¼šå­”åˆ‡å‰²æ·±åº¦å¿…é¡»å¤§äºŽç­‰äºŽ 0</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1887"/>
      <source>Hole error: Invalid countersink</source>
      <translation>å­”é”™è¯¯ï¼šæ— æ•ˆçš„åŸ‹å¤´å­”</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1923"/>
      <source>Hole error: Invalid drill point angle</source>
      <translation>å­”é”™è¯¯ï¼šæ— æ•ˆçš„é’»å°–è§’åº¦</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1940"/>
      <source>Hole error: Invalid drill point</source>
      <translation>å­”é”™è¯¯ï¼šé’»ç‚¹æ— æ•ˆ</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1977"/>
      <source>Hole error: Could not revolve sketch</source>
      <translation>å­”é”™è¯¯ï¼šæ— æ³•æ—‹è½¬è‰å›¾</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="1984"/>
      <source>Hole error: Resulting shape is empty</source>
      <translation>å­”é”™è¯¯ï¼šç»“æžœå½¢çŠ¶ä¸ºç©º</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="2007"/>
      <source>Hole error: Finding axis failed</source>
      <translation>å­”é”™è¯¯ï¼šæŸ¥æ‰¾è½´å¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="2073"/>
      <location filename="../../../App/FeatureHole.cpp" line="2081"/>
      <source>Boolean operation failed on profile Edge</source>
      <translation>è½®å»“è¾¹ç¼˜å¸ƒå°”è¿ç®—å¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="2088"/>
      <source>Boolean operation produced non-solid on profile Edge</source>
      <translation>åœ¨è½®å»“è¾¹ç¼˜çš„å¸ƒå°”è¿ç®—äº§ç”Ÿäº†éžå®žä½“</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureBoolean.cpp" line="153"/>
      <source>Boolean operation failed</source>
      <translation>å¸ƒå°”æ“ä½œå¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="2114"/>
      <source>Could not create face from sketch.
Intersecting sketch entities or multiple faces in a sketch are not allowed for making a pocket up to a face.</source>
      <translation>æ— æ³•ä»Žè‰å›¾åˆ›å»ºé¢ã€‚ä¸å…è®¸ä½¿ç”¨ç›¸äº¤çš„è‰å›¾å®žä½“ã€æˆ–è‰å›¾ä¸­çš„å¤šä¸ªé¢æ¥åˆ¶ä½œå‡¹æ§½ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="2280"/>
      <source>Thread type out of range</source>
      <translation>èžºçº¿ç±»åž‹è¶…å‡ºèŒƒå›´</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="2283"/>
      <source>Thread size out of range</source>
      <translation>èžºçº¿å¤§å°è¶…å‡ºèŒƒå›´</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureHole.cpp" line="2431"/>
      <source>Error: Thread could not be built</source>
      <translation>é”™è¯¯ï¼šæ— æ³•æž„å»ºèžºçº¹</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureLoft.cpp" line="193"/>
      <source>Loft: At least one section is needed</source>
      <translation>æ‹‰ä¼¸ï¼šè‡³å°‘éœ€è¦ä¸€ä¸ªè½®å»Š</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureLoft.cpp" line="394"/>
      <source>Loft: A fatal error occurred when making the loft</source>
      <translation>æ‹‰ä¼¸ï¼šåœ¨æ‹‰ä¼¸æ—¶å‘ç”Ÿè‡´å‘½é”™è¯¯</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureLoft.cpp" line="240"/>
      <source>Loft: Creating a face from sketch failed</source>
      <translation>æ‹‰ä¼¸ï¼šä»Žè‰å›¾åˆ›å»ºé¢å¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureLoft.cpp" line="303"/>
      <location filename="../../../App/FeaturePipe.cpp" line="446"/>
      <source>Loft: Failed to create shell</source>
      <translation>æ‹‰ä¼¸ï¼šåˆ›å»ºå¤–å£³å¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureExtrude.cpp" line="819"/>
      <source>Could not create face from sketch.
Intersecting sketch entities or multiple faces in a sketch are not allowed.</source>
      <translation>æ— æ³•ä»Žè‰å›¾ç«‹å»ºé¢ã€‚
è‰å›¾ä¸­ä¸å…è®¸æœ‰ç›¸äº¤çš„å®žä½“æˆ–å¤šä¸ªé¢ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="205"/>
      <source>Pipe: Could not obtain profile shape</source>
      <translation>ç®¡é“ï¼šæ— æ³•èŽ·å–è½®å»“å½¢çŠ¶</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="212"/>
      <source>No spine linked</source>
      <translation>æ²¡é“¾æŽ¥åˆ°éª¨æž¶</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="227"/>
      <source>No auxiliary spine linked.</source>
      <translation>æ²¡é“¾æŽ¥åˆ°è¾…åŠ©éª¨æž¶ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="250"/>
      <source>Pipe: Only one isolated point is needed if using a sketch with isolated points for section</source>
      <translation>ç®¡é“ï¼šåœ¨ä½¿ç”¨å¸¦æœ‰å­¤ç«‹ç‚¹çš„è‰å›¾ä½œä¸ºæˆªé¢æ—¶ï¼Œåªéœ€è¦ä¸€ä¸ªå­¤ç«‹ç‚¹ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="259"/>
      <source>Pipe: At least one section is needed when using a single point for profile</source>
      <translation>ç®¡é“ï¼šå½“ä½¿ç”¨å•ç‚¹è½®å»“æ—¶ï¼Œè‡³å°‘éœ€è¦ä¸€ä¸ªæˆªé¢</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="277"/>
      <source>Pipe: All sections need to be Part features</source>
      <translation>ç®¡é“ï¼šæ‰€æœ‰æˆªé¢éƒ½éœ€è¦æ˜¯é›¶ä»¶ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="285"/>
      <source>Pipe: Could not obtain section shape</source>
      <translation>ç®¡é“ï¼šæ— æ³•èŽ·å–æˆªé¢å½¢çŠ¶</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="295"/>
      <source>Pipe: Only the profile and last section can be vertices</source>
      <translation>ç®¡é“ï¼šåªæœ‰è½®å»“å’Œæœ€åŽä¸€ä¸ªæˆªé¢å¯ä»¥ä½œä¸ºé¡¶ç‚¹</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="308"/>
      <source>Multisections need to have the same amount of inner wires as the base section</source>
      <translation>å¤šé‡æˆªé¢éœ€è¦æœ‰ä¸ŽåŸºæœ¬æˆªé¢ç›¸åŒæ•°é‡çš„å†…éƒ¨çº¿</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="341"/>
      <source>Path must not be a null shape</source>
      <translation>è·¯å¾„ä¸èƒ½æ˜¯ç©ºå½¢çŠ¶</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="381"/>
      <source>Pipe could not be built</source>
      <translation>æ— æ³•æž„å»ºç®¡é“</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="438"/>
      <source>Result is not a solid</source>
      <translation>ç»“æžœä¸æ˜¯å®žä½“</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="477"/>
      <source>Pipe: There is nothing to subtract from</source>
      <translation>é”™è¯¯: æ²¡æœ‰å¯å‡å°‘çš„å†…å®¹</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="545"/>
      <source>A fatal error occurred when making the pipe</source>
      <translation>åˆ¶ä½œç®¡é“æ—¶å‘ç”Ÿè‡´å‘½é”™è¯¯</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="674"/>
      <source>Invalid element in spine.</source>
      <translation>éª¨æž¶ä¸­æœ‰æ— æ•ˆå…ƒç´ ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="679"/>
      <source>Element in spine is neither an edge nor a wire.</source>
      <translation>éª¨æž¶ä¸­çš„å…ƒç´ æ—¢ä¸æ˜¯è¾¹çº¿ä¹Ÿä¸æ˜¯è¿žçº¿ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="700"/>
      <source>Spine is not connected.</source>
      <translation>éª¨æž¶æœªè¿žæŽ¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="706"/>
      <source>Spine is neither an edge nor a wire.</source>
      <translation>éª¨æž¶æ—¢ä¸æ˜¯è¾¹çº¿ä¹Ÿä¸æ˜¯è¿žçº¿ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePipe.cpp" line="711"/>
      <source>Invalid spine.</source>
      <translation>æ— æ•ˆéª¨æž¶ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="103"/>
      <source>Cannot subtract primitive feature without base feature</source>
      <translation>æ²¡æœ‰åŸºç¡€ç‰¹å¾æ—¶æ— æ³•å‡åŽ»åŽŸå§‹ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureLoft.cpp" line="355"/>
      <location filename="../../../App/FeaturePipe.cpp" line="507"/>
      <location filename="../../../App/FeaturePrimitive.cpp" line="125"/>
      <source>Unknown operation type</source>
      <translation>æœªçŸ¥æ“ä½œç±»åž‹</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureLoft.cpp" line="363"/>
      <location filename="../../../App/FeaturePipe.cpp" line="515"/>
      <location filename="../../../App/FeaturePrimitive.cpp" line="133"/>
      <source>Failed to perform boolean operation</source>
      <translation>æ‰§è¡Œå¸ƒå°”æ“ä½œå¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="217"/>
      <source>Length of box too small</source>
      <translation>æ–¹å—é•¿åº¦è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="222"/>
      <source>Width of box too small</source>
      <translation>æ–¹å—å®½åº¦è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="227"/>
      <source>Height of box too small</source>
      <translation>æ–¹å—é«˜åº¦è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="275"/>
      <source>Radius of cylinder too small</source>
      <translation>åœ†æŸ±åŠå¾„è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="280"/>
      <source>Height of cylinder too small</source>
      <translation>åœ†æŸ±é«˜åº¦è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="285"/>
      <source>Rotation angle of cylinder too small</source>
      <translation>åœ†æŸ±æ—‹è½¬è§’åº¦è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="342"/>
      <source>Radius of sphere too small</source>
      <translation>çƒä½“åŠå¾„è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="394"/>
      <location filename="../../../App/FeaturePrimitive.cpp" line="399"/>
      <source>Radius of cone cannot be negative</source>
      <translation>é”¥ä½“åŠå¾„ä¸èƒ½ä¸ºè´Ÿæ•°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="404"/>
      <source>Height of cone too small</source>
      <translation>é”¥ä½“é«˜åº¦å¤ªå°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="484"/>
      <location filename="../../../App/FeaturePrimitive.cpp" line="489"/>
      <source>Radius of ellipsoid too small</source>
      <translation>æ¤­çƒåŠå¾„è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="583"/>
      <location filename="../../../App/FeaturePrimitive.cpp" line="588"/>
      <source>Radius of torus too small</source>
      <translation>çŽ¯é¢åŠå¾„è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="673"/>
      <source>Polygon of prism is invalid, must have 3 or more sides</source>
      <translation>æ£±æŸ±çš„å¤šè¾¹å½¢æ— æ•ˆï¼Œå¿…é¡»è‡³å°‘æœ‰ 3 æ¡æˆ–ä»¥ä¸Šçš„è¾¹</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="678"/>
      <source>Circumradius of the polygon, of the prism, is too small</source>
      <translation>æ£±æŸ±å¤šè¾¹å½¢çš„å¤–æŽ¥åœ†åŠå¾„è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="683"/>
      <source>Height of prism is too small</source>
      <translation>æ£±æŸ±é«˜åº¦è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="770"/>
      <source>delta x of wedge too small</source>
      <translation>æ¥”å½¢çš„ X å·®è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="776"/>
      <source>delta y of wedge too small</source>
      <translation>æ¥”å½¢çš„ Y å·®è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="782"/>
      <source>delta z of wedge too small</source>
      <translation>æ¥”å½¢çš„ Z å·®è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="788"/>
      <source>delta z2 of wedge is negative</source>
      <translation>æ¥”å½¢çš„ Z2 å·®æ˜¯è´Ÿæ•°</translation>
    </message>
    <message>
      <location filename="../../../App/FeaturePrimitive.cpp" line="794"/>
      <source>delta x2 of wedge is negative</source>
      <translation>æ¥”å½¢çš„ X2 å·®æ˜¯è´Ÿæ•°</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureRevolved.cpp" line="96"/>
      <source>Angle of revolution too large</source>
      <translation>æ—‹è½¬è§’è¿‡å¤§</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureRevolved.cpp" line="103"/>
      <source>Angle of revolution too small</source>
      <translation>æ—‹è½¬è§’è¿‡å°</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureRevolved.cpp" line="110"/>
      <source>Angles of revolution nullify each other</source>
      <translation>æ—‹è½¬çš„è§’åº¦ç›¸äº’æŠµæ¶ˆ</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureRevolved.cpp" line="126"/>
      <source>Reference axis is invalid</source>
      <translation>å‚è€ƒåæ ‡è½´æ— æ•ˆ</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureExtrude.cpp" line="758"/>
      <source>Fusion with base feature failed</source>
      <translation>ä¸ŽåŸºæœ¬ç‰¹å¾è”åˆå¤±è´¥</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureTransformed.cpp" line="101"/>
      <source>Transformation feature Linked object is not a Part object</source>
      <translation>è½¬æ¢åŠŸèƒ½é“¾æŽ¥çš„ä¸æ˜¯é›¶ä»¶å¯¹è±¡</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureTransformed.cpp" line="109"/>
      <source>No features selected to be mirrored.</source>
      <translation>æ²¡æœ‰é€‰ä¸­ä»»ä½•è¦è¿›è¡Œé•œåƒçš„ç‰¹å¾ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureTransformed.cpp" line="112"/>
      <source>No features selected to be patterned.</source>
      <translation>æ²¡æœ‰é€‰ä¸­ä»»ä½•è¦è¿›è¡Œé˜µåˆ—çš„ç‰¹å¾ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureTransformed.cpp" line="115"/>
      <source>No features selected to be transformed.</source>
      <translation>æ²¡æœ‰é€‰ä¸­ä»»ä½•è¦è¿›è¡Œå˜æ¢çš„ç‰¹å¾ã€‚</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureTransformed.cpp" line="356"/>
      <source>Cannot transform invalid support shape</source>
      <translation>æ— æ³•å˜æ¢æ— æ•ˆçš„æ”¯æŒå½¢çŠ¶</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureTransformed.cpp" line="407"/>
      <source>Shape of additive/subtractive feature is empty</source>
      <translation>æ·»åŠ /å‡æ–™çš„ç‰¹æ€§å½¢çŠ¶ä¸ºç©º</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureTransformed.cpp" line="398"/>
      <source>Only additive and subtractive features can be transformed</source>
      <translation>åªèƒ½å˜æ¢å¢žæ–™å’Œå‡æ–™ç‰¹å¾</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureThickness.cpp" line="109"/>
      <source>Invalid face reference</source>
      <translation>æ— æ•ˆçš„é¢å‚è€ƒ</translation>
    </message>
  </context>
  <context>
    <name>PartDesign_InvoluteGear</name>
    <message>
      <location filename="../../../InvoluteGearFeature.py" line="62"/>
      <source>Involute Gear</source>
      <translation>æ¸å¼€çº¿é½¿è½®</translation>
    </message>
    <message>
      <location filename="../../../InvoluteGearFeature.py" line="66"/>
      <source>Creates or edits the involute gear definition</source>
      <translation>åˆ›å»ºæˆ–ç¼–è¾‘æ¸å¼€çº¿é½¿è½®å®šä¹‰</translation>
    </message>
  </context>
  <context>
    <name>PartDesign_Sprocket</name>
    <message>
      <location filename="../../../SprocketFeature.py" line="65"/>
      <source>Sprocket</source>
      <translation>é“¾è½®</translation>
    </message>
    <message>
      <location filename="../../../SprocketFeature.py" line="69"/>
      <source>Creates or edits the sprocket definition.</source>
      <translation>åˆ›å»ºæˆ–ç¼–è¾‘é“¾è½®å®šä¹‰ã€‚</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskPreviewParameters</name>
    <message>
      <location filename="../../TaskPreviewParameters.ui" line="20"/>
      <source>Show final result</source>
      <translation>æ˜¾ç¤ºæœ€ç»ˆç»“æžœ</translation>
    </message>
    <message>
      <location filename="../../TaskPreviewParameters.ui" line="27"/>
      <source>Show preview overlay</source>
      <translation>æ˜¾ç¤ºé¢„è§ˆè¦†ç›–</translation>
    </message>
    <message>
      <location filename="../../TaskFeatureParameters.cpp" line="50"/>
      <source>Preview</source>
      <translation>é¢„è§ˆ</translation>
    </message>
  </context>
  <context>
    <name>PartDesign_WizardShaft</name>
    <message>
      <location filename="../../../WizardShaft/WizardShaft.py" line="225"/>
      <source>Shaft Design Wizard</source>
      <translation>è½´è®¾è®¡å‘å¯¼</translation>
    </message>
    <message>
      <location filename="../../../WizardShaft/WizardShaft.py" line="228"/>
      <source>Starts the shaft design wizard</source>
      <translation>å¯åŠ¨è½´è®¾è®¡å‘å¯¼</translation>
    </message>
  </context>
  <context>
    <name>PartDesign::FeatureAddSub</name>
    <message>
      <location filename="../../../App/FeatureAddSub.cpp" line="87"/>
      <source>Failure while computing removed volume preview: %1</source>
      <translation>è®¡ç®—ç§»é™¤ä½“ç§¯é¢„è§ˆæ—¶å‡ºé”™ï¼š%1</translation>
    </message>
    <message>
      <location filename="../../../App/FeatureAddSub.cpp" line="125"/>
      <source>Resulting shape is empty. That may indicate that no material will be removed or a problem with the model.</source>
      <translation>ç»“æžœå½¢çŠ¶ä¸ºç©ºã€‚è¿™å¯èƒ½è¡¨ç¤ºä¸ä¼šç§»é™¤ä»»ä½•ææ–™æˆ–æ¨¡åž‹å­˜åœ¨é—®é¢˜ã€‚</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignCompDatums</name>
    <message>
      <location filename="../../Command.cpp" line="2648"/>
      <source>Create Datum</source>
      <translation>åˆ›å»ºåŸºå‡†</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2649"/>
      <source>Creates a datum object or local coordinate system</source>
      <translation>åˆ›å»ºåŸºå‡†å¯¹è±¡æˆ–å±€éƒ¨åæ ‡ç³»</translation>
    </message>
  </context>
  <context>
    <name>CmdPartDesignCompSketches</name>
    <message>
      <location filename="../../Command.cpp" line="2683"/>
      <source>Create Datum</source>
      <translation>åˆ›å»ºåŸºå‡†</translation>
    </message>
    <message>
      <location filename="../../Command.cpp" line="2684"/>
      <source>Creates a datum object or local coordinate system</source>
      <translation>åˆ›å»ºåŸºå‡†å¯¹è±¡æˆ–å±€éƒ¨åæ ‡ç³»</translation>
    </message>
  </context>
  <context>
    <name>PartDesign_CompPrimitiveAdditive</name>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="217"/>
      <source>Creates an additive box by its width, height, and length</source>
      <translation>é€šè¿‡å®½åº¦ã€é«˜åº¦å’Œé•¿åº¦åˆ›å»ºåŠ æ³•ç›’</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="226"/>
      <source>Creates an additive cylinder by its radius, height, and angle</source>
      <translation>é€šè¿‡åŠå¾„ã€é«˜åº¦å’Œè§’åº¦åˆ›å»ºåŠ æ³•åœ†æŸ±ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="235"/>
      <source>Creates an additive sphere by its radius and various angles</source>
      <translation>é€šè¿‡åŠå¾„å’Œå„ç§è§’åº¦åˆ›å»ºåŠ æ³•çƒä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="244"/>
      <source>Creates an additive cone</source>
      <translation>åˆ›å»ºåŠ æ³•é”¥ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="250"/>
      <source>Creates an additive ellipsoid</source>
      <translation>åˆ›å»ºåŠ æ³•æ¤­çƒä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="256"/>
      <source>Creates an additive torus</source>
      <translation>åˆ›å»ºåŠ æ³•çŽ¯é¢</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="262"/>
      <source>Creates an additive prism</source>
      <translation>åˆ›å»ºåŠ æ³•æ£±æŸ±ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="268"/>
      <source>Creates an additive wedge</source>
      <translation>åˆ›å»ºåŠ æ³•æ¥”å½¢ä½“</translation>
    </message>
  </context>
  <context>
    <name>PartDesign_CompPrimitiveSubtractive</name>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="402"/>
      <source>Creates a subtractive box by its width, height and length</source>
      <translation>é€šè¿‡å®½åº¦ã€é«˜åº¦å’Œé•¿åº¦åˆ›å»ºå‡æ³•ç›’</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="411"/>
      <source>Creates a subtractive cylinder by its radius, height and angle</source>
      <translation>é€šè¿‡åŠå¾„ã€é«˜åº¦å’Œè§’åº¦åˆ›å»ºå‡æ³•åœ†æŸ±ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="420"/>
      <source>Creates a subtractive sphere by its radius and various angles</source>
      <translation>é€šè¿‡åŠå¾„å’Œå„ç§è§’åº¦åˆ›å»ºå‡æ³•çƒä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="429"/>
      <source>Creates a subtractive cone</source>
      <translation>åˆ›å»ºå‡æ³•é”¥ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="435"/>
      <source>Creates a subtractive ellipsoid</source>
      <translation>åˆ›å»ºå‡æ³•æ¤­çƒä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="441"/>
      <source>Creates a subtractive torus</source>
      <translation>åˆ›å»ºå‡æ³•çŽ¯é¢</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="447"/>
      <source>Creates a subtractive prism</source>
      <translation>åˆ›å»ºå‡æ³•æ£±æŸ±ä½“</translation>
    </message>
    <message>
      <location filename="../../CommandPrimitive.cpp" line="453"/>
      <source>Creates a subtractive wedge</source>
      <translation>åˆ›å»ºå‡æ³•æ¥”å½¢ä½“</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskDlgPrimitiveParameters</name>
    <message>
      <location filename="../../TaskPrimitiveParameters.cpp" line="1082"/>
      <source>Attachment</source>
      <translation>é™„ç€</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskDlgRevolutionParameters</name>
    <message>
      <location filename="../../TaskRevolutionParameters.cpp" line="802"/>
      <source>Revolution Parameters</source>
      <translation>æ—‹è½¬å‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskDlgGrooveParameters</name>
    <message>
      <location filename="../../TaskRevolutionParameters.cpp" line="812"/>
      <source>Groove Parameters</source>
      <translation>æ§½å‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskTransformedMessages</name>
    <message>
      <location filename="../../TaskTransformedMessages.cpp" line="39"/>
      <source>Transformed Feature Messages</source>
      <translation>å˜æ¢ç‰¹å¾æ¶ˆæ¯</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::ViewProviderBody</name>
    <message>
      <location filename="../../ViewProviderBody.cpp" line="199"/>
      <source>Active Body</source>
      <translation>æ´»åŠ¨å®žä½“</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::ViewProviderChamfer</name>
    <message>
      <location filename="../../ViewProviderChamfer.h" line="44"/>
      <source>Chamfer Parameters</source>
      <translation>å€’è§’å‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::ViewProviderDatum</name>
    <message>
      <location filename="../../ViewProviderDatum.cpp" line="115"/>
      <source>Datum Plane Parameters</source>
      <translation>åŸºå‡†é¢å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../ViewProviderDatum.cpp" line="120"/>
      <source>Datum Line Parameters</source>
      <translation>åŸºå‡†çº¿å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../ViewProviderDatum.cpp" line="125"/>
      <source>Datum Point Parameters</source>
      <translation>åŸºå‡†ç‚¹å‚æ•°</translation>
    </message>
    <message>
      <location filename="../../ViewProviderDatum.cpp" line="130"/>
      <source>Local Coordinate System Parameters</source>
      <translation>å±€éƒ¨åæ ‡ç³»å‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::ViewProviderDraft</name>
    <message>
      <location filename="../../ViewProviderDraft.h" line="45"/>
      <source>Draft Parameters</source>
      <translation>æ”¾æ ·å‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::ViewProviderFillet</name>
    <message>
      <location filename="../../ViewProviderFillet.h" line="44"/>
      <source>Fillet Parameters</source>
      <translation>åœ†è§’å‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::ViewProviderLinearPattern</name>
    <message>
      <location filename="../../ViewProviderLinearPattern.h" line="41"/>
      <source>Linear Pattern Parameters</source>
      <translation>çº¿æ€§é˜µåˆ—å‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGuii::ViewProviderMirrored</name>
    <message>
      <location filename="../../ViewProviderMirrored.h" line="41"/>
      <source>Mirror Parameters</source>
      <translation>é•œåƒå‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::ViewProviderMultiTransform</name>
    <message>
      <location filename="../../ViewProviderMultiTransform.h" line="41"/>
      <source>Multi-Transform Parameters</source>
      <translation>å¤šé‡å˜æ¢å‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::ViewProviderPolarPattern</name>
    <message>
      <location filename="../../ViewProviderPolarPattern.h" line="41"/>
      <source>Polar Pattern Parameters</source>
      <translation>æžè½´é˜µåˆ—å‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::ViewProviderScaled</name>
    <message>
      <location filename="../../ViewProviderScaled.h" line="41"/>
      <source>Scale Parameters</source>
      <translation>ç¼©æ”¾å‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::ViewProviderThickness</name>
    <message>
      <location filename="../../ViewProviderThickness.h" line="44"/>
      <source>Thickness Parameters</source>
      <translation>åŽšåº¦å‚æ•°</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskPatternParameters</name>
    <message>
      <location filename="../../TaskPatternParameters.cpp" line="132"/>
      <source>Direction 2</source>
      <translation>æ–¹å‘ 2</translation>
    </message>
    <message>
      <location filename="../../TaskPatternParameters.cpp" line="248"/>
      <source>Select a direction reference (edge, face, datum line)</source>
      <translation>é€‰æ‹©ä¸€ä¸ªæ–¹å‘å‚è€ƒï¼ˆè¾¹ã€é¢ã€åŸºå‡†çº¿ï¼‰</translation>
    </message>
    <message>
      <location filename="../../TaskPatternParameters.cpp" line="334"/>
      <source>Invalid selection. Select an edge, planar face, or datum line.</source>
      <translation>æ— æ•ˆé€‰æ‹©ã€‚é€‰æ‹©ä¸€æ¡è¾¹ã€ä¸€ä¸ªå¹³é¢æˆ–ä¸€æ¡åŸºå‡†çº¿ã€‚</translation>
    </message>
  </context>
  <context>
    <name>PartDesignGui::TaskDlgFeatureParameters</name>
    <message>
      <location filename="../../TaskFeatureParameters.cpp" line="229"/>
      <source>The feature could not be created with the given parameters.
The geometry may be invalid or the parameters may be incompatible.
Please adjust the parameters and try again.</source>
      <translation>æ— æ³•ä½¿ç”¨ç»™å®šçš„å‚æ•°åˆ›å»ºè¯¥ç‰¹å¾ã€‚
å‡ ä½•å›¾å½¢å¯èƒ½æ— æ•ˆæˆ–å‚æ•°å¯èƒ½ä¸å…¼å®¹ã€‚
è¯·è°ƒæ•´å‚æ•°å¹¶é‡è¯•ã€‚</translation>
    </message>
  </context>
</TS>

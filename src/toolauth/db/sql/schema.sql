-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'tool'
-- 
-- ---

DROP TABLE IF EXISTS `tool`;
		
CREATE TABLE `tool` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `drupal_name` MEDIUMTEXT(128) NOT NULL
);

-- ---
-- Table 'base'
-- 
-- ---

DROP TABLE IF EXISTS `base`;
		
CREATE TABLE `base` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` MEDIUMTEXT(128) NOT NULL,
  `mac_addr` MEDIUMTEXT(128) NULL DEFAULT NULL,
  `ip_addr` MEDIUMTEXT(128) NULL DEFAULT NULL,
  `encrypt_pass` MEDIUMTEXT(128) NULL DEFAULT NULL,
  `ota_pass` MEDIUMTEXT(64) NULL DEFAULT NULL,
  `has_reader` INTEGER NOT NULL DEFAULT 1,
  `is_vacuum` INTEGER NOT NULL DEFAULT 0,
  `tool_id` INTEGER NULL DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL
);

-- ---
-- Table 'session_core'
-- 
-- ---

DROP TABLE IF EXISTS `session_core`;
		
CREATE TABLE `session_core` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `card_id` MEDIUMTEXT(128) NOT NULL,
  `member_id` INTEGER NOT NULL, 
  `member_name` MEDIUMTEXT(128) NULL DEFAULT NULL,
  `reader_id` INTEGER NOT NULL,
  `reader_name` MEDIUMTEXT(128) NOT NULL, 
  `tool_id` INTEGER NULL DEFAULT NULL,
  `tool_name` MEDIUMTEXT(128) NULL DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL
);

-- ---
-- Table 'session_event'
-- 
-- ---

DROP TABLE IF EXISTS `session_event`;
		
CREATE TABLE `session_event` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `session_id` INTEGER NOT NULL, 
  `action` MEDIUMTEXT(128) NULL DEFAULT NULL,
  `active_session` INTEGER NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP NOT NULL
);

-- ---
-- Table 'reader_to_tool'
-- 
-- ---

DROP TABLE IF EXISTS `reader_to_tool`;
		
CREATE TABLE `reader_to_tool` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `reader_id` INTEGER NOT NULL,
  `tool_id` INTEGER NOT NULL,
  `created_at` TIMESTAMP NOT NULL
);

-- ---
-- Table 'tool_to_vacuum'
-- 
-- ---

DROP TABLE IF EXISTS `tool_to_vacuum`;
		
CREATE TABLE `tool_to_vacuum` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `tool_id` INTEGER NOT NULL,
  `vacuum_id` INTEGER NOT NULL,
  `created_at` TIMESTAMP NOT NULL
);

-- ---
-- Foreign Keys 
-- ---  ============================================== Not working

ALTER TABLE `base` ADD FOREIGN KEY (`reader_id`) REFERENCES `reader` (`id`);
ALTER TABLE `base` ADD FOREIGN KEY (`tool_id`)   REFERENCES `tool` (`id`);
ALTER TABLE `reader_to_tool` ADD FOREIGN KEY (`reader_id`) REFERENCES `reader` (`id`);
ALTER TABLE `reader_to_tool` ADD FOREIGN KEY (`tool_id`)   REFERENCES `tool` (`id`);
ALTER TABLE `tool_to_vacuum` ADD FOREIGN KEY (`tool_id`)   REFERENCES `tool` (`id`);
ALTER TABLE `tool_to_vacuum` ADD FOREIGN KEY (`vacuum_id`) REFERENCES `base` (`id`);
ALTER TABLE `session_event` ADD FOREIGN KEY (`session_id`) REFERENCES `session_core` (`id`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `tool` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `base` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `reader` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `reader_to_tool` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `tool_to_vacuum` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `tool` (`id`,`drupal_name`) VALUES
-- ('','');
-- INSERT INTO `base` (`id`,`name`,`mac_addr`,`ip_addr`,`encrypt_pass`,`ota_pass`,`reader_id`,`tool_id`,`created_at`) VALUES
-- ('','','','','','','','','');
-- INSERT INTO `reader` (`id`) VALUES
-- ('');
-- INSERT INTO `reader_to_tool` (`id`,`reader_id`,`tool_id`,`created_at`) VALUES
-- ('','','','');
-- INSERT INTO `tool_to_vacuum` (`id`,`tool_id`,`vacuum_id`,`created_at`) VALUES
-- ('','','','');
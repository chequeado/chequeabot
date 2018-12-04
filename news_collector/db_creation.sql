CREATE DATABASE `newscollector_db` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;
CREATE TABLE `feed_entries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(500) DEFAULT NULL,
  `source` varchar(45) DEFAULT NULL,
  `seccion` varchar(140) DEFAULT NULL,
  `entry_date` datetime DEFAULT NULL,
  `format` varchar(45) DEFAULT NULL,
  `title` longtext,
  `entry_text` longtext,
  `source_type` varchar(45) DEFAULT 'newspaper',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2749 DEFAULT CHARSET=utf8;

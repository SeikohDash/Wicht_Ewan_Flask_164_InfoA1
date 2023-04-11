-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: wicht_ewan_infoa1_pharmacie

-- Destruction de la BD si elle existe.
-- Pour être certain d'avoir la dernière version des données

DROP DATABASE IF EXISTS wicht_ewan_infoa1_pharmacie;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS wicht_ewan_infoa1_pharmacie;

-- Utilisation de cette base de donnée

USE wicht_ewan_infoa1_pharmacie;
-- --------------------------------------------------------
-- --------------------------------------------------------
-- Hôte :                        localhost
-- Version du serveur:           8.0.31 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Export de la structure de la base pour wicht_ewan_infoa1_pharmacie
CREATE DATABASE IF NOT EXISTS `wicht_ewan_infoa1_pharmacie` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `wicht_ewan_infoa1_pharmacie`;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_achat
CREATE TABLE IF NOT EXISTS `t_achat` (
  `id_achat` int NOT NULL AUTO_INCREMENT,
  `fk-objets` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id_achat`),
  KEY `FK_t_achat_objets` (`fk-objets`),
  CONSTRAINT `FK_t_achat_objets` FOREIGN KEY (`fk-objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_achat : ~0 rows (environ)
/*!40000 ALTER TABLE `t_achat` DISABLE KEYS */;
INSERT INTO `t_achat` (`id_achat`, `fk-objets`, `date`) VALUES
	(1, 1, '2023-03-13');
/*!40000 ALTER TABLE `t_achat` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_achat_client
CREATE TABLE IF NOT EXISTS `t_achat_client` (
  `id_achat_client` int NOT NULL AUTO_INCREMENT,
  `date_achat` date DEFAULT NULL,
  `nombre_medic` int DEFAULT NULL,
  `nom_medic` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_achat_client`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_achat_client : ~0 rows (environ)
/*!40000 ALTER TABLE `t_achat_client` DISABLE KEYS */;
INSERT INTO `t_achat_client` (`id_achat_client`, `date_achat`, `nombre_medic`, `nom_medic`) VALUES
	(1, '2023-02-01', 3, 'dafalgan');
/*!40000 ALTER TABLE `t_achat_client` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_adresse
CREATE TABLE IF NOT EXISTS `t_adresse` (
  `id_adresse` int NOT NULL AUTO_INCREMENT,
  `nom_rue` varchar(50) DEFAULT NULL,
  `NPA` varchar(50) DEFAULT NULL,
  `Localite` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_adresse`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_adresse : ~0 rows (environ)
/*!40000 ALTER TABLE `t_adresse` DISABLE KEYS */;
INSERT INTO `t_adresse` (`id_adresse`, `nom_rue`, `NPA`, `Localite`) VALUES
	(1, 'Route d\'Yverdon', '1033', 'cheseaux');
/*!40000 ALTER TABLE `t_adresse` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_client
CREATE TABLE IF NOT EXISTS `t_client` (
  `id_client` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) DEFAULT NULL,
  `prenom` varchar(50) DEFAULT NULL,
  `date_de_nais` date DEFAULT NULL,
  `fk_genre` int DEFAULT NULL,
  `Assu_maladie` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_client`),
  KEY `fk_genre` (`fk_genre`),
  CONSTRAINT `fk_genre` FOREIGN KEY (`fk_genre`) REFERENCES `t_genre` (`id_genre`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_client : ~0 rows (environ)
/*!40000 ALTER TABLE `t_client` DISABLE KEYS */;
INSERT INTO `t_client` (`id_client`, `nom`, `prenom`, `date_de_nais`, `fk_genre`, `Assu_maladie`) VALUES
	(1, 'Wicht', 'Ewan', '2006-07-06', 1, 'VD');
/*!40000 ALTER TABLE `t_client` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_fournisseur
CREATE TABLE IF NOT EXISTS `t_fournisseur` (
  `id_fournisseur` int NOT NULL AUTO_INCREMENT,
  `nom_four` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_fournisseur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_fournisseur : ~0 rows (environ)
/*!40000 ALTER TABLE `t_fournisseur` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_fournisseur` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_genre
CREATE TABLE IF NOT EXISTS `t_genre` (
  `id_genre` int NOT NULL AUTO_INCREMENT,
  `nom_genre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_genre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_genre : ~3 rows (environ)
/*!40000 ALTER TABLE `t_genre` DISABLE KEYS */;
INSERT INTO `t_genre` (`id_genre`, `nom_genre`) VALUES
	(1, 'M'),
	(2, 'F'),
	(4, 'lo');
/*!40000 ALTER TABLE `t_genre` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_mail
CREATE TABLE IF NOT EXISTS `t_mail` (
  `id_mail` int NOT NULL AUTO_INCREMENT,
  `nom-mail` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_mail`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_mail : ~0 rows (environ)
/*!40000 ALTER TABLE `t_mail` DISABLE KEYS */;
INSERT INTO `t_mail` (`id_mail`, `nom-mail`) VALUES
	(1, 'e.wicht@gmail.com');
/*!40000 ALTER TABLE `t_mail` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_mise_en_stock
CREATE TABLE IF NOT EXISTS `t_mise_en_stock` (
  `id_mise_en_stock` int NOT NULL AUTO_INCREMENT,
  `fk-objets` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `nb_objets` int DEFAULT NULL,
  PRIMARY KEY (`id_mise_en_stock`),
  KEY `FK_t_mise_en_stock_objets` (`fk-objets`),
  CONSTRAINT `FK_t_mise_en_stock_objets` FOREIGN KEY (`fk-objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_mise_en_stock : ~0 rows (environ)
/*!40000 ALTER TABLE `t_mise_en_stock` DISABLE KEYS */;
INSERT INTO `t_mise_en_stock` (`id_mise_en_stock`, `fk-objets`, `date`, `nb_objets`) VALUES
	(1, 1, '2023-03-13', 10);
/*!40000 ALTER TABLE `t_mise_en_stock` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_objets
CREATE TABLE IF NOT EXISTS `t_objets` (
  `id_objets` int NOT NULL AUTO_INCREMENT,
  `medic` varchar(50) DEFAULT NULL,
  `vaccin` varchar(50) DEFAULT NULL,
  `perimer` varchar(50) DEFAULT NULL,
  `cb_ean` int DEFAULT NULL,
  `prix` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_objets`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_objets : ~0 rows (environ)
/*!40000 ALTER TABLE `t_objets` DISABLE KEYS */;
INSERT INTO `t_objets` (`id_objets`, `medic`, `vaccin`, `perimer`, `cb_ean`, `prix`) VALUES
	(1, 'dafalgan', NULL, NULL, 101101, '10.-');
/*!40000 ALTER TABLE `t_objets` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_pers_achat_client
CREATE TABLE IF NOT EXISTS `t_pers_achat_client` (
  `id_pers_achat_client` int NOT NULL AUTO_INCREMENT,
  `fk-client` int DEFAULT NULL,
  `fk-achat_client` int DEFAULT NULL,
  PRIMARY KEY (`id_pers_achat_client`),
  KEY `FK_t_pers_achat_client_achat_client` (`fk-achat_client`),
  KEY `FK_t_pers_achat_client_client` (`fk-client`),
  CONSTRAINT `FK_t_pers_achat_client_achat_client` FOREIGN KEY (`fk-achat_client`) REFERENCES `t_achat_client` (`id_achat_client`),
  CONSTRAINT `FK_t_pers_achat_client_client` FOREIGN KEY (`fk-client`) REFERENCES `t_client` (`id_client`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_pers_achat_client : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_achat_client` DISABLE KEYS */;
INSERT INTO `t_pers_achat_client` (`id_pers_achat_client`, `fk-client`, `fk-achat_client`) VALUES
	(1, 1, 1);
/*!40000 ALTER TABLE `t_pers_achat_client` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_pers_adresse
CREATE TABLE IF NOT EXISTS `t_pers_adresse` (
  `id_pers_adresse` int NOT NULL AUTO_INCREMENT,
  `fk-client` int DEFAULT NULL,
  `fk-adresse` int DEFAULT NULL,
  PRIMARY KEY (`id_pers_adresse`),
  KEY `FK_t_pers_adresse_client` (`fk-client`),
  KEY `FK_t_pers_adresse_adresse` (`fk-adresse`),
  CONSTRAINT `FK_t_pers_adresse_adresse` FOREIGN KEY (`fk-adresse`) REFERENCES `t_adresse` (`id_adresse`),
  CONSTRAINT `FK_t_pers_adresse_client` FOREIGN KEY (`fk-client`) REFERENCES `t_client` (`id_client`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_pers_adresse : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_adresse` DISABLE KEYS */;
INSERT INTO `t_pers_adresse` (`id_pers_adresse`, `fk-client`, `fk-adresse`) VALUES
	(1, 1, 1);
/*!40000 ALTER TABLE `t_pers_adresse` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_pers_mail
CREATE TABLE IF NOT EXISTS `t_pers_mail` (
  `id_pers_mail` int NOT NULL AUTO_INCREMENT,
  `fk-client` int DEFAULT NULL,
  `fk-mail` int DEFAULT NULL,
  PRIMARY KEY (`id_pers_mail`),
  KEY `FK_t_pers_mail_client` (`fk-client`),
  KEY `FK_t_pers_mail_mail` (`fk-mail`),
  CONSTRAINT `FK_t_pers_mail_client` FOREIGN KEY (`fk-client`) REFERENCES `t_client` (`id_client`),
  CONSTRAINT `FK_t_pers_mail_mail` FOREIGN KEY (`fk-mail`) REFERENCES `t_mail` (`id_mail`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_pers_mail : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_mail` DISABLE KEYS */;
INSERT INTO `t_pers_mail` (`id_pers_mail`, `fk-client`, `fk-mail`) VALUES
	(1, 1, 1);
/*!40000 ALTER TABLE `t_pers_mail` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_pers_telephone
CREATE TABLE IF NOT EXISTS `t_pers_telephone` (
  `id_pers_telephone` int NOT NULL AUTO_INCREMENT,
  `fk-client` int DEFAULT NULL,
  `fk-telephone` int DEFAULT NULL,
  PRIMARY KEY (`id_pers_telephone`),
  KEY `FK_t_pers_telephone_client` (`fk-client`),
  KEY `FK_t_pers_telephone_telephone` (`fk-telephone`),
  CONSTRAINT `FK_t_pers_telephone_client` FOREIGN KEY (`fk-client`) REFERENCES `t_client` (`id_client`),
  CONSTRAINT `FK_t_pers_telephone_telephone` FOREIGN KEY (`fk-telephone`) REFERENCES `t_telephone` (`id_telephone`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_pers_telephone : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_telephone` DISABLE KEYS */;
INSERT INTO `t_pers_telephone` (`id_pers_telephone`, `fk-client`, `fk-telephone`) VALUES
	(1, 1, 1);
/*!40000 ALTER TABLE `t_pers_telephone` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_pers_traitement
CREATE TABLE IF NOT EXISTS `t_pers_traitement` (
  `id_pers_traitement` int NOT NULL AUTO_INCREMENT,
  `fk-client` int NOT NULL DEFAULT '0',
  `fk-traitement` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_pers_traitement`),
  KEY `fk-client` (`fk-client`),
  KEY `fk-traitement` (`fk-traitement`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_pers_traitement : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_traitement` DISABLE KEYS */;
INSERT INTO `t_pers_traitement` (`id_pers_traitement`, `fk-client`, `fk-traitement`) VALUES
	(1, 1, 1);
/*!40000 ALTER TABLE `t_pers_traitement` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_reception
CREATE TABLE IF NOT EXISTS `t_reception` (
  `id_reception` int NOT NULL AUTO_INCREMENT,
  `fk-objets` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id_reception`),
  KEY `FK_t_reception_objets` (`fk-objets`),
  CONSTRAINT `FK_t_reception_objets` FOREIGN KEY (`fk-objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_reception : ~0 rows (environ)
/*!40000 ALTER TABLE `t_reception` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_reception` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_retour_client
CREATE TABLE IF NOT EXISTS `t_retour_client` (
  `id_retourner` int NOT NULL AUTO_INCREMENT,
  `fk-objets` int DEFAULT NULL,
  PRIMARY KEY (`id_retourner`),
  KEY `FK__objets` (`fk-objets`),
  CONSTRAINT `FK__objets` FOREIGN KEY (`fk-objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_retour_client : ~0 rows (environ)
/*!40000 ALTER TABLE `t_retour_client` DISABLE KEYS */;
INSERT INTO `t_retour_client` (`id_retourner`, `fk-objets`) VALUES
	(1, 1);
/*!40000 ALTER TABLE `t_retour_client` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_retour_objets
CREATE TABLE IF NOT EXISTS `t_retour_objets` (
  `id_retour_objets` int NOT NULL AUTO_INCREMENT,
  `fk-objets` int DEFAULT NULL,
  `fk-fournisseur` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id_retour_objets`),
  KEY `FK_t_retour_objets_objets` (`fk-objets`),
  KEY `FK_t_retour_objets_fournisseur` (`fk-fournisseur`),
  CONSTRAINT `FK_t_retour_objets_fournisseur` FOREIGN KEY (`fk-fournisseur`) REFERENCES `t_fournisseur` (`id_fournisseur`),
  CONSTRAINT `FK_t_retour_objets_objets` FOREIGN KEY (`fk-objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_retour_objets : ~0 rows (environ)
/*!40000 ALTER TABLE `t_retour_objets` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_retour_objets` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_retrait_du_stock
CREATE TABLE IF NOT EXISTS `t_retrait_du_stock` (
  `id_retrait_du_stock` int NOT NULL AUTO_INCREMENT,
  `fk-objets` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `nb_objets` int DEFAULT NULL,
  PRIMARY KEY (`id_retrait_du_stock`),
  KEY `FK_t_retrait_du_stock_objets` (`fk-objets`),
  CONSTRAINT `FK_t_retrait_du_stock_objets` FOREIGN KEY (`fk-objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_retrait_du_stock : ~0 rows (environ)
/*!40000 ALTER TABLE `t_retrait_du_stock` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_retrait_du_stock` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_stock
CREATE TABLE IF NOT EXISTS `t_stock` (
  `id_stock` int NOT NULL AUTO_INCREMENT,
  `fk-objets` int DEFAULT NULL,
  `emplacement` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_stock`),
  KEY `FK_stock_objets` (`fk-objets`),
  CONSTRAINT `FK_stock_objets` FOREIGN KEY (`fk-objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_stock : ~0 rows (environ)
/*!40000 ALTER TABLE `t_stock` DISABLE KEYS */;
INSERT INTO `t_stock` (`id_stock`, `fk-objets`, `emplacement`) VALUES
	(1, 1, 'A2');
/*!40000 ALTER TABLE `t_stock` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_telephone
CREATE TABLE IF NOT EXISTS `t_telephone` (
  `id_telephone` int NOT NULL AUTO_INCREMENT,
  `num_tel` varchar(50) DEFAULT NULL,
  `indicatif` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_telephone`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_telephone : ~0 rows (environ)
/*!40000 ALTER TABLE `t_telephone` DISABLE KEYS */;
INSERT INTO `t_telephone` (`id_telephone`, `num_tel`, `indicatif`) VALUES
	(1, '079 123 01 02', '41');
/*!40000 ALTER TABLE `t_telephone` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_traitement
CREATE TABLE IF NOT EXISTS `t_traitement` (
  `id_traitement` int NOT NULL AUTO_INCREMENT,
  `Ordonnance` varchar(50) DEFAULT NULL,
  `type_traitement` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_traitement`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_traitement : ~0 rows (environ)
/*!40000 ALTER TABLE `t_traitement` DISABLE KEYS */;
INSERT INTO `t_traitement` (`id_traitement`, `Ordonnance`, `type_traitement`) VALUES
	(1, 'CH', 'permanent');
/*!40000 ALTER TABLE `t_traitement` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_vendu_client
CREATE TABLE IF NOT EXISTS `t_vendu_client` (
  `id_vendu` int NOT NULL AUTO_INCREMENT,
  `fk-objets` int DEFAULT NULL,
  PRIMARY KEY (`id_vendu`),
  KEY `FK_t_vendu_objets` (`fk-objets`),
  CONSTRAINT `FK_t_vendu_objets` FOREIGN KEY (`fk-objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_vendu_client : ~0 rows (environ)
/*!40000 ALTER TABLE `t_vendu_client` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_vendu_client` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_vols
CREATE TABLE IF NOT EXISTS `t_vols` (
  `id_vols` int NOT NULL AUTO_INCREMENT,
  `fk-objets` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `nb_objets` int DEFAULT NULL,
  PRIMARY KEY (`id_vols`),
  KEY `FK_t_vols_objets` (`fk-objets`),
  CONSTRAINT `FK_t_vols_objets` FOREIGN KEY (`fk-objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_vols : ~0 rows (environ)
/*!40000 ALTER TABLE `t_vols` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_vols` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

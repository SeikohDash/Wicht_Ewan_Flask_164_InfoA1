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
  `date_achat` date DEFAULT NULL,
  `nombre_objets` int DEFAULT NULL,
  `nom_objets` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_achat`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_achat : ~2 rows (environ)
/*!40000 ALTER TABLE `t_achat` DISABLE KEYS */;
INSERT INTO `t_achat` (`id_achat`, `date_achat`, `nombre_objets`, `nom_objets`) VALUES
	(1, '2023-02-01', 3, 'dafalgan'),
	(2, '2023-05-04', 5, 'bepanthen ');
/*!40000 ALTER TABLE `t_achat` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_achat_objets
CREATE TABLE IF NOT EXISTS `t_achat_objets` (
  `id_achat` int NOT NULL AUTO_INCREMENT,
  `fk_objets` int DEFAULT NULL,
  `prix_achat` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id_achat`),
  KEY `FK_t_achat_objets` (`fk_objets`),
  CONSTRAINT `FK_t_achat_objets` FOREIGN KEY (`fk_objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_achat_objets : ~3 rows (environ)
/*!40000 ALTER TABLE `t_achat_objets` DISABLE KEYS */;
INSERT INTO `t_achat_objets` (`id_achat`, `fk_objets`, `prix_achat`, `date`) VALUES
	(1, 1, '25.-', '2023-03-13'),
	(2, 5, '40.-', '2023-05-14'),
	(3, 3, '50.-', '2023-05-14');
/*!40000 ALTER TABLE `t_achat_objets` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_adresse
CREATE TABLE IF NOT EXISTS `t_adresse` (
  `id_adresse` int NOT NULL AUTO_INCREMENT,
  `nom_rue` varchar(50) DEFAULT NULL,
  `NPA` varchar(50) DEFAULT NULL,
  `Localite` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_adresse`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_adresse : ~3 rows (environ)
/*!40000 ALTER TABLE `t_adresse` DISABLE KEYS */;
INSERT INTO `t_adresse` (`id_adresse`, `nom_rue`, `NPA`, `Localite`) VALUES
	(1, 'Route d\'Yverdon 10b', '1033', 'Cheseaux'),
	(2, 'Pl. de l\'Hôtel de Ville 1 ', '1041', 'Echallens'),
	(3, 'Rue du Village 9 ', '1121', ' Bremblens');
/*!40000 ALTER TABLE `t_adresse` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_assurance
CREATE TABLE IF NOT EXISTS `t_assurance` (
  `id_assu` int NOT NULL AUTO_INCREMENT,
  `nom_assu` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_assu`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_assurance : ~5 rows (environ)
/*!40000 ALTER TABLE `t_assurance` DISABLE KEYS */;
INSERT INTO `t_assurance` (`id_assu`, `nom_assu`) VALUES
	(1, 'Assura'),
	(2, 'Helsana'),
	(3, 'Visana'),
	(4, 'Sanitas'),
	(5, 'Aturpi');
/*!40000 ALTER TABLE `t_assurance` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_client
CREATE TABLE IF NOT EXISTS `t_client` (
  `id_client` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) DEFAULT NULL,
  `prenom` varchar(50) DEFAULT NULL,
  `date_de_nais` date DEFAULT NULL,
  `fk_genre` int DEFAULT NULL,
  `fk_assu` int DEFAULT NULL,
  PRIMARY KEY (`id_client`),
  KEY `fk_genre` (`fk_genre`),
  KEY `FK_t_client_t_assurance` (`fk_assu`),
  CONSTRAINT `fk_genre` FOREIGN KEY (`fk_genre`) REFERENCES `t_genre` (`id_genre`),
  CONSTRAINT `FK_t_client_t_assurance` FOREIGN KEY (`fk_assu`) REFERENCES `t_assurance` (`id_assu`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_client : ~5 rows (environ)
/*!40000 ALTER TABLE `t_client` DISABLE KEYS */;
INSERT INTO `t_client` (`id_client`, `nom`, `prenom`, `date_de_nais`, `fk_genre`, `fk_assu`) VALUES
	(2, 'Loic', 'lolo', '2001-01-01', 1, 2),
	(3, 'LOLO', 'Ewan', '2023-04-13', 2, 1),
	(4, 'Eric', 'Fabio', '2005-12-05', 1, 3),
	(5, 'Wicht', 'Stephane', '2004-03-03', 1, 5),
	(6, 'Meric', 'Lilou', '2005-12-05', 2, 1);
/*!40000 ALTER TABLE `t_client` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_fournisseur
CREATE TABLE IF NOT EXISTS `t_fournisseur` (
  `id_fournisseur` int NOT NULL AUTO_INCREMENT,
  `nom_four` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_fournisseur`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_fournisseur : ~5 rows (environ)
/*!40000 ALTER TABLE `t_fournisseur` DISABLE KEYS */;
INSERT INTO `t_fournisseur` (`id_fournisseur`, `nom_four`) VALUES
	(1, 'Abbott'),
	(2, 'Accel'),
	(3, 'Baxter'),
	(4, 'Celltrion'),
	(5, 'Genzyme');
/*!40000 ALTER TABLE `t_fournisseur` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_fournisseur_objets
CREATE TABLE IF NOT EXISTS `t_fournisseur_objets` (
  `t_fournisseur_objets` int NOT NULL AUTO_INCREMENT,
  `fk_objets` int DEFAULT NULL,
  `fk_fourn` int DEFAULT NULL,
  PRIMARY KEY (`t_fournisseur_objets`),
  KEY `FK_t_reception_objets` (`fk_objets`),
  KEY `FK_t_objets_reception_fourn_t_fournisseur` (`fk_fourn`),
  CONSTRAINT `FK_t_objets_reception_fourn_t_fournisseur` FOREIGN KEY (`fk_fourn`) REFERENCES `t_fournisseur` (`id_fournisseur`),
  CONSTRAINT `FK_t_reception_objets` FOREIGN KEY (`fk_objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_fournisseur_objets : ~10 rows (environ)
/*!40000 ALTER TABLE `t_fournisseur_objets` DISABLE KEYS */;
INSERT INTO `t_fournisseur_objets` (`t_fournisseur_objets`, `fk_objets`, `fk_fourn`) VALUES
	(1, 4, 2),
	(2, 2, 3),
	(3, 1, 4),
	(4, 1, 3),
	(6, 3, 2),
	(7, 5, 1),
	(8, 5, 2),
	(9, 5, 3),
	(10, 5, 4),
	(11, 5, 5);
/*!40000 ALTER TABLE `t_fournisseur_objets` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_genre
CREATE TABLE IF NOT EXISTS `t_genre` (
  `id_genre` int NOT NULL AUTO_INCREMENT,
  `nom_genre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_genre`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_genre : ~3 rows (environ)
/*!40000 ALTER TABLE `t_genre` DISABLE KEYS */;
INSERT INTO `t_genre` (`id_genre`, `nom_genre`) VALUES
	(1, 'homme'),
	(2, 'femme'),
	(3, 'autre');
/*!40000 ALTER TABLE `t_genre` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_mail
CREATE TABLE IF NOT EXISTS `t_mail` (
  `id_mail` int NOT NULL AUTO_INCREMENT,
  `nom_mail` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_mail`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_mail : ~3 rows (environ)
/*!40000 ALTER TABLE `t_mail` DISABLE KEYS */;
INSERT INTO `t_mail` (`id_mail`, `nom_mail`) VALUES
	(1, 'e.wicht@gmail.com'),
	(2, 'maccaud@eduvaud.ch'),
	(3, 'Eric.lulu@apple.com');
/*!40000 ALTER TABLE `t_mail` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_objets
CREATE TABLE IF NOT EXISTS `t_objets` (
  `id_objets` int NOT NULL AUTO_INCREMENT,
  `nom_objets` varchar(50) DEFAULT NULL,
  `cb_ean` int DEFAULT NULL,
  `prix` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_objets`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_objets : ~5 rows (environ)
/*!40000 ALTER TABLE `t_objets` DISABLE KEYS */;
INSERT INTO `t_objets` (`id_objets`, `nom_objets`, `cb_ean`, `prix`) VALUES
	(1, 'dafalgan', 101101, '10.-'),
	(2, 'COVID-19', 10011, '50.-'),
	(3, 'Somnifères', 100101, '25.-'),
	(4, 'bepanthen', 10100, '20.-'),
	(5, 'Sirop pour la toux', 100011, '55.-');
/*!40000 ALTER TABLE `t_objets` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_pers_achat_client
CREATE TABLE IF NOT EXISTS `t_pers_achat_client` (
  `id_pers_achat_client` int NOT NULL AUTO_INCREMENT,
  `fk_client` int DEFAULT NULL,
  `fk_achat` int DEFAULT NULL,
  PRIMARY KEY (`id_pers_achat_client`),
  KEY `FK_t_pers_achat_client_achat_client` (`fk_achat`),
  KEY `FK_t_pers_achat_client_client` (`fk_client`),
  CONSTRAINT `FK_t_pers_achat_client_achat_client` FOREIGN KEY (`fk_achat`) REFERENCES `t_achat` (`id_achat`),
  CONSTRAINT `FK_t_pers_achat_client_client` FOREIGN KEY (`fk_client`) REFERENCES `t_client` (`id_client`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_pers_achat_client : ~2 rows (environ)
/*!40000 ALTER TABLE `t_pers_achat_client` DISABLE KEYS */;
INSERT INTO `t_pers_achat_client` (`id_pers_achat_client`, `fk_client`, `fk_achat`) VALUES
	(1, 5, 1),
	(2, 3, 1);
/*!40000 ALTER TABLE `t_pers_achat_client` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_pers_adresse
CREATE TABLE IF NOT EXISTS `t_pers_adresse` (
  `id_pers_adresse` int NOT NULL AUTO_INCREMENT,
  `fk_client` int DEFAULT NULL,
  `fk_adresse` int DEFAULT NULL,
  PRIMARY KEY (`id_pers_adresse`),
  KEY `FK_t_pers_adresse_client` (`fk_client`),
  KEY `FK_t_pers_adresse_adresse` (`fk_adresse`),
  CONSTRAINT `FK_t_pers_adresse_adresse` FOREIGN KEY (`fk_adresse`) REFERENCES `t_adresse` (`id_adresse`),
  CONSTRAINT `FK_t_pers_adresse_client` FOREIGN KEY (`fk_client`) REFERENCES `t_client` (`id_client`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_pers_adresse : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_adresse` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_pers_adresse` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_pers_mail
CREATE TABLE IF NOT EXISTS `t_pers_mail` (
  `id_pers_mail` int NOT NULL AUTO_INCREMENT,
  `fk_client` int DEFAULT NULL,
  `fk_mail` int DEFAULT NULL,
  PRIMARY KEY (`id_pers_mail`),
  KEY `FK_t_pers_mail_client` (`fk_client`),
  KEY `FK_t_pers_mail_mail` (`fk_mail`),
  CONSTRAINT `FK_t_pers_mail_client` FOREIGN KEY (`fk_client`) REFERENCES `t_client` (`id_client`),
  CONSTRAINT `FK_t_pers_mail_mail` FOREIGN KEY (`fk_mail`) REFERENCES `t_mail` (`id_mail`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_pers_mail : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_mail` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_pers_mail` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_pers_telephone
CREATE TABLE IF NOT EXISTS `t_pers_telephone` (
  `id_pers_telephone` int NOT NULL AUTO_INCREMENT,
  `fk_client` int DEFAULT NULL,
  `fk_telephone` int DEFAULT NULL,
  PRIMARY KEY (`id_pers_telephone`),
  KEY `FK_t_pers_telephone_client` (`fk_client`),
  KEY `FK_t_pers_telephone_telephone` (`fk_telephone`),
  CONSTRAINT `FK_t_pers_telephone_client` FOREIGN KEY (`fk_client`) REFERENCES `t_client` (`id_client`),
  CONSTRAINT `FK_t_pers_telephone_telephone` FOREIGN KEY (`fk_telephone`) REFERENCES `t_telephone` (`id_telephone`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_pers_telephone : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_telephone` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_pers_telephone` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_pers_traitement
CREATE TABLE IF NOT EXISTS `t_pers_traitement` (
  `id_pers_traitement` int NOT NULL AUTO_INCREMENT,
  `fk_client` int NOT NULL DEFAULT '0',
  `fk_traitement` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_pers_traitement`),
  KEY `fk-client` (`fk_client`),
  KEY `fk-traitement` (`fk_traitement`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_pers_traitement : ~0 rows (environ)
/*!40000 ALTER TABLE `t_pers_traitement` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_pers_traitement` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_retour_client
CREATE TABLE IF NOT EXISTS `t_retour_client` (
  `id_retourner` int NOT NULL AUTO_INCREMENT,
  `fk_objets` int DEFAULT NULL,
  `fk_client` int DEFAULT NULL,
  PRIMARY KEY (`id_retourner`),
  KEY `FK__objets` (`fk_objets`),
  KEY `FK_t_retour_client_t_client` (`fk_client`),
  CONSTRAINT `FK__objets` FOREIGN KEY (`fk_objets`) REFERENCES `t_objets` (`id_objets`),
  CONSTRAINT `FK_t_retour_client_t_client` FOREIGN KEY (`fk_client`) REFERENCES `t_client` (`id_client`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_retour_client : ~0 rows (environ)
/*!40000 ALTER TABLE `t_retour_client` DISABLE KEYS */;
INSERT INTO `t_retour_client` (`id_retourner`, `fk_objets`, `fk_client`) VALUES
	(1, 1, NULL);
/*!40000 ALTER TABLE `t_retour_client` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_retour_objets
CREATE TABLE IF NOT EXISTS `t_retour_objets` (
  `id_retour_objets` int NOT NULL AUTO_INCREMENT,
  `fk_objets` int DEFAULT NULL,
  `fk_fournisseur` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id_retour_objets`),
  KEY `FK_t_retour_objets_objets` (`fk_objets`),
  KEY `FK_t_retour_objets_fournisseur` (`fk_fournisseur`),
  CONSTRAINT `FK_t_retour_objets_fournisseur` FOREIGN KEY (`fk_fournisseur`) REFERENCES `t_fournisseur` (`id_fournisseur`),
  CONSTRAINT `FK_t_retour_objets_objets` FOREIGN KEY (`fk_objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_retour_objets : ~0 rows (environ)
/*!40000 ALTER TABLE `t_retour_objets` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_retour_objets` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_retrait_du_stock
CREATE TABLE IF NOT EXISTS `t_retrait_du_stock` (
  `id_retrait_du_stock` int NOT NULL AUTO_INCREMENT,
  `fk_objets` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `nb_objets` int DEFAULT NULL,
  PRIMARY KEY (`id_retrait_du_stock`),
  KEY `FK_t_retrait_du_stock_objets` (`fk_objets`),
  CONSTRAINT `FK_t_retrait_du_stock_objets` FOREIGN KEY (`fk_objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_retrait_du_stock : ~0 rows (environ)
/*!40000 ALTER TABLE `t_retrait_du_stock` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_retrait_du_stock` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_stock
CREATE TABLE IF NOT EXISTS `t_stock` (
  `id_stock` int NOT NULL AUTO_INCREMENT,
  `emplacement` varchar(50) DEFAULT NULL,
  `nb_objets` int DEFAULT NULL,
  PRIMARY KEY (`id_stock`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_stock : ~0 rows (environ)
/*!40000 ALTER TABLE `t_stock` DISABLE KEYS */;
INSERT INTO `t_stock` (`id_stock`, `emplacement`, `nb_objets`) VALUES
	(1, 'A2', NULL);
/*!40000 ALTER TABLE `t_stock` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_stock_objets
CREATE TABLE IF NOT EXISTS `t_stock_objets` (
  `id_stock_objets` int NOT NULL AUTO_INCREMENT,
  `fk_objets` int DEFAULT NULL,
  `fk_stock` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id_stock_objets`),
  KEY `FK_t_mise_en_stock_objets` (`fk_objets`),
  KEY `FK_t_mise_en_stock_t_stock` (`fk_stock`),
  CONSTRAINT `FK_t_mise_en_stock_objets` FOREIGN KEY (`fk_objets`) REFERENCES `t_objets` (`id_objets`),
  CONSTRAINT `FK_t_mise_en_stock_t_stock` FOREIGN KEY (`fk_stock`) REFERENCES `t_stock` (`id_stock`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_stock_objets : ~0 rows (environ)
/*!40000 ALTER TABLE `t_stock_objets` DISABLE KEYS */;
INSERT INTO `t_stock_objets` (`id_stock_objets`, `fk_objets`, `fk_stock`, `date`) VALUES
	(1, 1, 1, '2023-03-13');
/*!40000 ALTER TABLE `t_stock_objets` ENABLE KEYS */;

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
  `fk_client` int NOT NULL DEFAULT '0',
  `fk_objets` int DEFAULT NULL,
  PRIMARY KEY (`id_vendu`),
  KEY `FK_t_vendu_objets` (`fk_objets`),
  KEY `FK_t_vendu_client_t_client` (`fk_client`),
  CONSTRAINT `FK_t_vendu_client_t_client` FOREIGN KEY (`fk_client`) REFERENCES `t_client` (`id_client`),
  CONSTRAINT `FK_t_vendu_objets` FOREIGN KEY (`fk_objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_vendu_client : ~0 rows (environ)
/*!40000 ALTER TABLE `t_vendu_client` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_vendu_client` ENABLE KEYS */;

-- Export de la structure de la table wicht_ewan_infoa1_pharmacie. t_vols
CREATE TABLE IF NOT EXISTS `t_vols` (
  `id_vols` int NOT NULL AUTO_INCREMENT,
  `fk_objets` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `nb_objets` int DEFAULT NULL,
  PRIMARY KEY (`id_vols`),
  KEY `FK_t_vols_objets` (`fk_objets`),
  CONSTRAINT `FK_t_vols_objets` FOREIGN KEY (`fk_objets`) REFERENCES `t_objets` (`id_objets`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Export de données de la table wicht_ewan_infoa1_pharmacie.t_vols : ~0 rows (environ)
/*!40000 ALTER TABLE `t_vols` DISABLE KEYS */;
INSERT INTO `t_vols` (`id_vols`, `fk_objets`, `date`, `nb_objets`) VALUES
	(1, 1, '2023-05-14', 10);
/*!40000 ALTER TABLE `t_vols` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

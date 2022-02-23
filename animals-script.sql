-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema animals_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `animals_schema` ;

-- -----------------------------------------------------
-- Schema animals_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `animals_schema` DEFAULT CHARACTER SET utf8 ;
USE `animals_schema` ;

-- -----------------------------------------------------
-- Table `animals_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `animals_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `animals_schema`.`animals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `animals_schema`.`animals` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `type` VARCHAR(45) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `animals_schema`.`shared_animals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `animals_schema`.`shared_animals` (
  `user_id` INT NOT NULL,
  `animal_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `animal_id`),
  INDEX `fk_users_has_animals_animals1_idx` (`animal_id` ASC) VISIBLE,
  INDEX `fk_users_has_animals_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_animals_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `animals_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_animals_animals1`
    FOREIGN KEY (`animal_id`)
    REFERENCES `animals_schema`.`animals` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

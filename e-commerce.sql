-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Usuario` (
  `IDUsuário` INT NOT NULL,
  `Nome` VARCHAR(100) NULL,
  `CPF` VARCHAR(14) NULL,
  `Email` VARCHAR(45) NULL,
  `Senha` VARCHAR(45) NULL,
  `Endereço` VARCHAR(45) NULL,
  `Telefone` VARCHAR(15) NULL,
  PRIMARY KEY (`IDUsuário`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Categoria` (
  `idCategoria` INT NOT NULL,
  `nome` VARCHAR(45) NULL,
  `descricao` VARCHAR(45) NULL,
  PRIMARY KEY (`idCategoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Produto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Produto` (
  `idProduto` INT NOT NULL,
  `Nome` VARCHAR(45) NULL,
  `Descrição` VARCHAR(45) NULL,
  `Preço` DECIMAL(10,2) NULL,
  `Quantidade em estoque` INT NULL,
  `Categoria` VARCHAR(45) NULL,
  `Categoria_idCategoria` INT NOT NULL,
  PRIMARY KEY (`idProduto`, `Categoria_idCategoria`),
  INDEX `fk_Produto_Categoria1_idx` (`Categoria_idCategoria` ASC) VISIBLE,
  CONSTRAINT `fk_Produto_Categoria1`
    FOREIGN KEY (`Categoria_idCategoria`)
    REFERENCES `mydb`.`Categoria` (`idCategoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Carrinho`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Carrinho` (
  `idCarrinho` INT NOT NULL,
  `Quantidade` INT NULL,
  `IDProduto` INT NOT NULL,
  PRIMARY KEY (`idCarrinho`, `IDProduto`),
  INDEX `fk_Carrinho_Produto_idx` (`IDProduto` ASC) VISIBLE,
  CONSTRAINT `fk_Carrinho_Produto`
    FOREIGN KEY (`IDProduto`)
    REFERENCES `mydb`.`Produto` (`idProduto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Pedido` (
  `idPedido` INT NOT NULL,
  `Data pedido` DATETIME NULL,
  `IDUsuário` INT NOT NULL,
  `Status pedido` VARCHAR(45) NULL,
  PRIMARY KEY (`idPedido`, `IDUsuário`),
  INDEX `fk_Pedido_Usuário1_idx` (`IDUsuário` ASC) VISIBLE,
  CONSTRAINT `fk_Pedido_Usuário1`
    FOREIGN KEY (`IDUsuário`)
    REFERENCES `mydb`.`Usuario` (`IDUsuário`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Item do pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Item do pedido` (
  `idItem do pedido` INT NOT NULL,
  `idPedido` INT NOT NULL,
  `idProduto` INT NOT NULL,
  `Quantidade` INT NULL,
  `Preço unitário` DECIMAL(10,2) NULL,
  PRIMARY KEY (`idItem do pedido`, `idPedido`, `idProduto`),
  INDEX `fk_Item do pedido_Pedido1_idx` (`idPedido` ASC) VISIBLE,
  INDEX `fk_Item do pedido_Produto1_idx` (`idProduto` ASC) VISIBLE,
  CONSTRAINT `fk_Item do pedido_Pedido1`
    FOREIGN KEY (`idPedido`)
    REFERENCES `mydb`.`Pedido` (`idPedido`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Item do pedido_Produto1`
    FOREIGN KEY (`idProduto`)
    REFERENCES `mydb`.`Produto` (`idProduto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Endereco`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Endereco` (
  `idEndereco` INT NOT NULL,
  `rua` VARCHAR(45) NULL,
  `numero` INT NULL,
  `cidade` VARCHAR(45) NULL,
  `estado` VARCHAR(45) NULL,
  `CEP` VARCHAR(45) NULL,
  `pais` VARCHAR(45) NULL,
  `Usuário_IDUsuário` INT NOT NULL,
  PRIMARY KEY (`idEndereco`, `Usuário_IDUsuário`),
  INDEX `fk_Endereco_Usuário1_idx` (`Usuário_IDUsuário` ASC) VISIBLE,
  CONSTRAINT `fk_Endereco_Usuário1`
    FOREIGN KEY (`Usuário_IDUsuário`)
    REFERENCES `mydb`.`Usuario` (`IDUsuário`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Pagamento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Pagamento` (
  `idPagamento` INT NOT NULL,
  `tipoPagamento` VARCHAR(45) NULL,
  `dataPagamento` DATETIME NULL,
  `status` VARCHAR(45) NULL,
  `valor` DECIMAL(10,2) NULL,
  `Pedido_idPedido` INT NOT NULL,
  PRIMARY KEY (`idPagamento`, `Pedido_idPedido`),
  INDEX `fk_Pagamento_Pedido1_idx` (`Pedido_idPedido` ASC) VISIBLE,
  CONSTRAINT `fk_Pagamento_Pedido1`
    FOREIGN KEY (`Pedido_idPedido`)
    REFERENCES `mydb`.`Pedido` (`idPedido`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

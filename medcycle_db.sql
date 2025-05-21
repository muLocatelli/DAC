-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 21/05/2025 às 16:53
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `medcycle_db`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `contatos`
--

CREATE TABLE `contatos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `assunto` varchar(255) DEFAULT NULL,
  `mensagem` text NOT NULL,
  `data_envio` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `descarte`
--

CREATE TABLE `descarte` (
  `id` int(11) NOT NULL,
  `data` date NOT NULL,
  `peso_kg` decimal(6,2) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `residuo_id` int(11) NOT NULL,
  `empresa_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `empresas_coletoras`
--

CREATE TABLE `empresas_coletoras` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `cnpj` varchar(18) NOT NULL,
  `licenca_ambiental` varchar(50) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `nao_conformidades`
--

CREATE TABLE `nao_conformidades` (
  `id` int(11) NOT NULL,
  `descarte_id` int(11) NOT NULL,
  `descricao` text NOT NULL,
  `data_ocorrencia` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `relatorios_agregados`
--

CREATE TABLE `relatorios_agregados` (
  `id` int(11) NOT NULL,
  `ano` int(11) DEFAULT NULL,
  `mes` int(11) DEFAULT NULL,
  `total_residuos_kg` decimal(10,2) DEFAULT NULL,
  `baixo_risco_kg` decimal(10,2) DEFAULT NULL,
  `medio_risco_kg` decimal(10,2) DEFAULT NULL,
  `alto_risco_kg` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `residuos`
--

CREATE TABLE `residuos` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `tipo` enum('Infectante','Perfurocortante','Químico','Reciclável') NOT NULL,
  `classificacao_risco` enum('Baixo','Médio','Alto') NOT NULL,
  `instrucoes` text NOT NULL,
  `setor_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `setores`
--

CREATE TABLE `setores` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) DEFAULT NULL,
  `sobrenome` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `cpf` varchar(14) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `cep` varchar(9) DEFAULT NULL,
  `senha_hash` varchar(255) DEFAULT NULL,
  `tipo` enum('admin','funcionario') DEFAULT 'funcionario',
  `data_cadastro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `contatos`
--
ALTER TABLE `contatos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Índices de tabela `descarte`
--
ALTER TABLE `descarte`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `residuo_id` (`residuo_id`),
  ADD KEY `empresa_id` (`empresa_id`);

--
-- Índices de tabela `empresas_coletoras`
--
ALTER TABLE `empresas_coletoras`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cnpj` (`cnpj`);

--
-- Índices de tabela `nao_conformidades`
--
ALTER TABLE `nao_conformidades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `descarte_id` (`descarte_id`);

--
-- Índices de tabela `relatorios_agregados`
--
ALTER TABLE `relatorios_agregados`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `residuos`
--
ALTER TABLE `residuos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `setor_id` (`setor_id`);

--
-- Índices de tabela `setores`
--
ALTER TABLE `setores`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `cpf` (`cpf`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `contatos`
--
ALTER TABLE `contatos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `descarte`
--
ALTER TABLE `descarte`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `empresas_coletoras`
--
ALTER TABLE `empresas_coletoras`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `nao_conformidades`
--
ALTER TABLE `nao_conformidades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `relatorios_agregados`
--
ALTER TABLE `relatorios_agregados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `residuos`
--
ALTER TABLE `residuos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `setores`
--
ALTER TABLE `setores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `contatos`
--
ALTER TABLE `contatos`
  ADD CONSTRAINT `contatos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Restrições para tabelas `descarte`
--
ALTER TABLE `descarte`
  ADD CONSTRAINT `descarte_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `descarte_ibfk_2` FOREIGN KEY (`residuo_id`) REFERENCES `residuos` (`id`),
  ADD CONSTRAINT `descarte_ibfk_3` FOREIGN KEY (`empresa_id`) REFERENCES `empresas_coletoras` (`id`);

--
-- Restrições para tabelas `nao_conformidades`
--
ALTER TABLE `nao_conformidades`
  ADD CONSTRAINT `nao_conformidades_ibfk_1` FOREIGN KEY (`descarte_id`) REFERENCES `descarte` (`id`);

--
-- Restrições para tabelas `residuos`
--
ALTER TABLE `residuos`
  ADD CONSTRAINT `residuos_ibfk_1` FOREIGN KEY (`setor_id`) REFERENCES `setores` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

## UEFS-ECOMP-TEC502-PBL01: Sistema de “Mercado Inteligente”

    Este repositório faz parte da solução do 1º problema da disciplina TEC502 - concorrência e conectividade, do curso de Engenharia de Computação (ECOMP), da Universidade Estadual de Feira de Santana (UEFS). Intitulado de sistema de “Mercado Inteligente”, o projeto visa trazer uma automatização para a etapa de avaliação e registro das compras nos supermercados. Para atingir essa automatização, faz-se uso de um sensor de etiquetas RFID, onde cada etiqueta (em teoria) faz o papel do código de barras de um produto dentro do sistema. Como o sensor permite a leitura simultânea de etiquetas/códigos de barras, as compras seriam agilizadas (por não haver mais a necessidade de leitura serial de códigos de barra), aumentando o fluxo dos caixas e contribuindo para a satisfação dos clientes, já que haverá uma diminuição do tempo de espera nas filas do caixa.

    Para construir o sistema, foram necessários 2 projetos distintos:

*   [Projeto do servidor central](https://github.com/Droid-M/TEC502-TP01-18111237-PBL01-API-DO-SUPERMERCADO) (api do mercado, disponível em “https://tec502-supermarket-test.000webhostapp.com/api”)
*   [Projeto das aplicações do caixa e do administrador](https://github.com/Droid-M/TEC502-TO1-PBL1-A18111237) (clientes diretos da api do mercado)

## Sobre este projeto (aplicações do caixa e do administrador)

   Enquanto o primeiro tópico traz uma visão geral da solução do problema, os próximos tópicos abaixo abordam especificamente o projeto neste repositório.

### **1\. Arquitetura**

#### **1.1. Bibliotecas de terceiros usadas no código python**

*   [paramiko](https://pypi.org/project/paramiko/) Para executar comandos na Raspberry Pi 0 via SSH
*   [requests](https://pypi.org/project/requests/) Para fazer requisições HTTPS à API central do mercado
*   [pytz](https://pypi.org/project/pytz/) Para ajustar o fuso horário dos valores vindos da API  (+0:00 h) ao fuso horário do Brasil (-3:00 h) e ajustar a formação da data
*   [keyboard](https://pypi.org/project/keyboard/) Para detectar a entrada do usuário e agir conforme a tecla pressionada, interrompendo eventos como o monitoramento de compras, por exemplo
*   [~pynput~](https://pypi.org/project/pynput/) Teria a mesma função da biblioteca `keyboard`, porém, devido a alguns conflitos durante o uso do docker, foi removida do projeto

#### **1.2. Ambientação**

Para executar o aplicativo de servidor manualmente na raspberry, siga os seguintes passos:

1.  Conecte-se à rede sem fio "LARSID" (sem aspas)
2.  No terminal, execute o comando `ssh tec502@172.16.103.0`
3.  Se a conexão for bem sucedida, insira a senha "larsid" (sem aspas)
4.  Navegue até a pasta Marcos através do comando `cd TP01/MarcOs`
5.  Verifique a presença dos arquivos "_server.py_" e “_server.env_” através do comando `ls`
6.  Execute o comando `python3 server.py`

#### **1.3. Estrutura de arquivos**

    Abaixo está a árvore de diretórios do projeto. Repare que este projeto apresenta tanto os arquivos necessários para o aplicativo do Caixa (ou caixista) quanto do Administrador. 

    O que difere qual aplicativo será executado ao executar a construção e o início do contêiner docker será a última linha presente no arquivo _Dockerfile_, presente na raiz do diretório. Para evitar sobrecarga de _Dockerfile_'s, duas branchs além da _main_ foram criadas: [_Cashier_](https://github.com/Droid-M/TEC502-TO1-PBL1-A18111237/tree/cashier) e [_Admin_](https://github.com/Droid-M/TEC502-TO1-PBL1-A18111237/tree/admin). A diferença principal entre as duas branchs está na última linha do Dockerfile. Na branch _Cashier_, a última linha corresponde à `CMD ["python3", "python/client/cashier_menu.py"]` enquanto na branch _Admin_ a última linha corresponde à `CMD ["python3", "python/client/admin_menu.py"]`. Dessa forma, quando for necessário executar a aplicação do caixista, basta clonar a branch _Cashier_ e quando for necessário executar a aplicação do administrador, basta clonar a branch _Admin_.

📦TEC502-TO1-PBL1-A18111237  
 ┣ 📂src  
 ┃ ┣ 📂python  
 ┃ ┃ ┣ 📂client  
 ┃ ┃ ┃ ┣ 📂cashier (pasta contendo o código da tela do caixa)  
 ┃ ┃ ┃ ┃ ┣ 📜manager.py (contém as funções que se comunicam com os endpoints do caixa, como registro de compra, pagamento, etc)  
 ┃ ┃ ┃ ┃ ┣ 📜menu.py (contém as opçoes do menu do caixa)  
 ┃ ┃ ┃ ┃ ┗ 📜\_\_init\_\_.py  
 ┃ ┃ ┃ ┣ 📂helpers (pasta contendo funções ajudantes. Essas funções são reutilizadas por todo código, portanto essa é uma das pastas fundamentais)  
 ┃ ┃ ┃ ┃ ┣ 📜dict.py  
 ┃ ┃ ┃ ┃ ┣ 📜file.py  
 ┃ ┃ ┃ ┃ ┣ 📜input.py  
 ┃ ┃ ┃ ┃ ┣ 📜menu.py  
 ┃ ┃ ┃ ┃ ┣ 📜request.py  
 ┃ ┃ ┃ ┃ ┣ 📜sensor.py  
 ┃ ┃ ┃ ┃ ┗ 📜\_\_init\_\_.py  
 ┃ ┃ ┃ ┣ 📂shop\_admin (pasta contendo o código da tela do administrador)  
 ┃ ┃ ┃ ┃ ┣ 📜configure\_raspberry.py (contém as funções responsáveis por copiar e executar arquivos na raspberry via _SSH_)  
 ┃ ┃ ┃ ┃ ┣ 📜manager.py  (contém as funções que acessam os endpoints do administrador)  
 ┃ ┃ ┃ ┃ ┣ 📜menu.py (contém as opções do menu do administrador)  
 ┃ ┃ ┃ ┃ ┣ 📜ssh\_open\_connection.py (contém as funções necessárias para iniciar e finalizar uma conexão _SSH_)  
 ┃ ┃ ┃ ┃ ┗ 📜\_\_init\_\_.py  
 ┃ ┃ ┃ ┣ 📜admin\_menu.py (script principal do programa do administrador)  
 ┃ ┃ ┃ ┣ 📜cashier\_menu.py (script principal do programa do caixista)  
 ┃ ┃ ┃ ┣ 📜run\_raspberry\_server.py  
 ┃ ┃ ┃ ┗ 📜\_\_init\_\_.py  
 ┃ ┃ ┣ 📂server  
 ┃ ┃ ┃ ┗ 📜raspberry\_server.py (arquivo que será executado na raspberry. Com ele a raspberry atuará como um servidor enviando as etiquetas lidas)  
 ┃ ┃ ┣ 📜.env (arquivo de ambientação usado para decidir qual arquivo de ambiente será lido (_local\_pc.env_ ou _raspberry.env_))  
 ┃ ┃ ┣ 📜local\_pc.env (arquivo de ambientação que contém os valos necessários para a execução dos programas no modo de simulação de sensor)  
 ┃ ┃ ┣ 📜raspberry.env (arquivo de ambientação que contém os valores necessários para a execução dos programas no modo de produção)  
 ┃ ┃ ┗ 📜\_\_init\_\_.py  
 ┃ ┗ 📜requirements.txt (contém as bibliotecas de terceiro usadas no projeto)  
 ┣ 📜.gitignore  
 ┣ 📜docker-compose.yml (desnecessário\* - permite montar um contêiner onde o _hot-reload_ de arquivos estará habilitado)  
 ┣ 📜Dockerfile (arquivo de configuração do ambiente docker)  
 ┣ 📜README.md  
 ┣ 📜run\_admin\_in\_linux.sh  
 ┣ 📜run\_admin\_in\_windows.bat  
 ┣ 📜run\_cashier\_in\_linux.sh  
 ┣ 📜run\_cashier\_in\_windows.bat  
 ┗ 📜run\_docker.sh (script para executar automaticamente os comandos de construção e execução do contêiner e imagem docker)

#### **1.4. Menu**

    Tanto as telas do caixista quanto as do administrador possuem o mesmo padrão comportamental e estrutural. A estrutura da primeira tela de ambos os programas é mais ou menos da seguinte forma:

1.  (Abre a tela de opções de caixista ou de administrador a depender do programa executado)
2.  Limpar console
3.  Sair
4.  Reiniciar

    O comportamento do menu de opções do caixista obedece a seguinte ordem: ler etiquetas → Validar e registrar compra → Pagar ou Cancelar compra. Já o comportamento do menu de opções do administrador não possui um fluxo restringente. Isso significa que qualquer opção pode ser selecionada, não importando a ordem (monitorar compra, histórico de compra, monitorar caixas, registrar produtos, bloquear caixa, etc.). 

   As **exceções** e **erros** que surgirem durante o uso do programa serão tratadas para evitar que o aplicativo quebre e uma mensagem de alerta é enviada ao usuário imediatamente. Em caso de exceções e erros relacionados à conexão com a internet, um aviso sobre a conexão é enviado ao usuário. Nos demais casos de erros e exceções, apenas uma sugestão é enviada ao usuário para que ele reinicie a aplicação (ironicamente, resolve a maioria dos casos).

#### **1.5. Estrutura e responsabilidades dos dispositivos na rede**

 O projeto foi planejado considerando que os dispositivos na rede adotariam a distribuição de responsabilidades conforme a **figura 1**, presente logo abaixo.

![Figura 1. Representação dos dispositivos na rede](https://33333.cdn.cke-cs.com/kSW7V9NHUXugvhoQeFaf/images/3ef54d59f8e549fc93f0f9a12f259c4f31dfaad2bdda4743.png)

                                                                                        **Figura 1.** Distribuição de responsabilidades dos dispositivos

    Conforme a distribuição e atribuição dos dispositivos, ficou determinado que o número de caixas pode ser qualquer um (o limite real seria o máximo que o banco de dados aguentar) enquanto haverá somente um administrador. A raspberry adotará a função de ‘sensor’ e ‘servidor’ (ou um servidor de sensoriamento). Tanto os caixas quanto o administrador consomem a API central. Não ficou registrado na figura por se tratar de uma ideia recente, mas, o caixa pode se comunicar com a raspberry também durante o registro de produtos na plataforma.

### **2\. Procolos**

#### **2.1. Comunicação com o sensor (raspberry)**

    A comunicação inicial feita com a raspberry é feita via _**SSH**_ através da biblioteca _paramiko_. Na comunicação inicial, 3 operações são executadas: enviar o arquivo ‘_server.py_’ para a raspberry; enviar o arquivo ‘_server.env_’ para a raspberry; executar o comando `python3 server.py` para iniciar o servidor do sersor na raspberry Pi 0.

    Enquanto o script '_server.py_' estiver em execução na raspberry, o "sensor" estará disponível para uso. E para usar acessar o sensor, ou seja, para acessar o servidor que está em execução na raspberry, uma conexão _**socket**_ é usada. Através da conexão _socket_, uma mensagem `**READ_SENSORS**` é enviada para o servidor na raspberry e esse servidor responde à mensagem enviando as etiquetas que forem lidas naquele instante.

   Após receber as etiquetas lidas, o caixa pode validar e registrar a compra. Para isso, uma conexão _**HTTPS**_ é iniciada com o servidor central do mercado e então as etiquetas (que aqui correspondem aos códigos de barra dos produtos) serão enviados via método _**Post**_ para o endpoint adequado.

### **3\. Conexões simultâneas**

#### **3.1. Threads**

     A API de sensoriamento em execução na raspberry trabalha com _multi-threads_ para processar as mensagens recebidas via _socket_. O uso de _sockets_ é para evitar que o servidor quebre ou fique lento para responder em caso de múltiplas requisições dos caixas à raspberry. Como efeito colateral, a quantidade de _timeouts_ por parte dos programas de caixa também foram reduzidos pelo uso de _threads_ no servidor de sensoriamento. Isto porque a conexão é aceita imediatamente pelo processo principal enquanto a tarefa de processar o pedido do _client_ é terceirizada para outra _thread “paralelamente”_ (na realidade, não é um paralelismo total, em boa parte do tempo é uma espécie de pseudo-paralelismo causado pela concorrência).

   A API central do mercado, construída com _PHP_, não lida diretamente com threads, porém, seu desempenho é tão alto que uma solicitação é recebida, tratada e respondida em milésimos de segundos (entre 150 e 280 milissegundos durante os testes). A explicação para um desempenho tão alto mesmo sem haver implementação de técnicas de otimização nem _threads_ no código é que todo processo de otimização, controle de entrada, processamento e otimização é efetuado automaticamente pelo [sistema do host](https://www.000webhost.com/) que está hospedando a API PHP.

### **4\. Transmissão de dados**

#### **4.1.  Troca de dados com o sensor (raspberry)**

    Como mencionado no subtópico **2.1**, a comunicação entre os caixas e a raspberry se dá por meio do _socket_. As mensagens enviadas pelo _client_ (caixas, administrador), são strings (conjunto de bytes) descritivas do que o servidor de sensoriamento deve fazer. No caso da mensagem `**READ_SENSORS**`**,** o servidor deve responder com as etiquetas que o sensor RFID ler naquele momento, porém, não será retornado uma lista propriamente dita, pois a conexão socket se limita à transmissão de strings. Então, para contornar a limitação e ainda enviar os IDs das etiquetas lidas, uma nova string é formada a partir da lista IDs de etiquetas lidas pelo sensor RFID onde cada ID é separado por uma vírgula (Ex: id1,id2,id3). Assim que a resposta é recebida, o _client_ (caixa) realiza um `response._split(',')_` na string para convertê-la de volta para uma lista de IDs.

     Já a comunicação entre o _client_ (caixa e administrador) e o _server_ (API central do mercado, escrita em PHP) é feita por strings padronizadas. O padrão estabelecido para organização dos dados dentro da string é conhecido como JSON. Toda codificação e decodificação da string para JSON e vice-versa é feita automaticamente pelas ferramentas oferecidas no _python_ e no _PHP_.

#### **4.2. Endpoints da api REST**

    Todos os endpoints usados na comunicação _REST_ com a API do mercado está disponível em "https://github.com/Droid-M/TEC502-TP01-18111237-PBL01-API-DO-SUPERMERCADO/tree/insomnia". Todas as rotas foram minuciosamente testadas através do programa _insomnia_. Para aprender a importar projetos do GitHub para o _insomnia_ consulte o link: [https://docs.insomnia.rest/insomnia/git-sync.](https://docs.insomnia.rest/insomnia/git-sync.)

### **Referências bibliográficas**

*   [https://www.geeksforgeeks.org/socket-programming-cc/](https://www.geeksforgeeks.org/socket-programming-cc/)
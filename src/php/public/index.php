<?php

require_once "../helpers/output_helpers.php";
require_once "../helpers/router_helpers.php";

$requestUri = parse_route(explode('?', $_SERVER['REQUEST_URI'])[0]);

// Define as rotas e suas respectivas ações
$routes = [
    '/user' => 'UserController',
    '/post' => 'PostController',
    // Adicione mais rotas aqui
];

dd($requestUri);

// Verifica se a rota existe
if (array_key_exists($requestUri, $routes)) {
    $controllerName = $routes[$requestUri];
    // Carrega o arquivo do controlador
    require_once("controllers/{$controllerName}.php");
    // Crie uma instância do controlador e chame um método para lidar com a solicitação
    $controller = new $controllerName();
    $controller->handleRequest();
} else {
    http_response_code(404);
    echo "404 - Not Found";
}

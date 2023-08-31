<?php

function parse_route($route)
{
    $paths = explode('/', $route);
    return array_reduce($paths, function ($acc, $path) {
        if (!$path) {
            return $acc;
        }
        if (!isset($acc[$path])) {
            $acc[$path] = array(
                'value' => $path,
                'children' => null
            );
        }
        $acc = &$acc[$path]['children'];
        return $acc ? $acc : array(
            'value' => $path,
            'children' => null
        );
    }, array());
}

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests básicos para verificar la estructura del bot
"""

import sys
import os

def test_imports():
    """Verifica que se puedan importar los módulos necesarios"""
    print("✓ Probando imports...")
    try:
        import slack_bolt
        print("  ✓ slack_bolt importado correctamente")
    except ImportError as e:
        print(f"  ✗ Error importando slack_bolt: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv importado correctamente")
    except ImportError as e:
        print(f"  ✗ Error importando python-dotenv: {e}")
        return False
    
    return True

def test_bot_structure():
    """Verifica que el archivo bot.py tenga la estructura correcta"""
    print("\n✓ Probando estructura del bot...")
    
    bot_file = "bot.py"
    if not os.path.exists(bot_file):
        print(f"  ✗ No se encuentra el archivo {bot_file}")
        return False
    
    with open(bot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar elementos clave
    required_elements = [
        ("Imports de Slack Bolt", "from slack_bolt import App"),
        ("Socket Mode Handler", "from slack_bolt.adapter.socket_mode import SocketModeHandler"),
        ("Logging", "import logging"),
        ("Dotenv", "from dotenv import load_dotenv"),
        ("Evento team_join", "@app.event(\"team_join\")"),
        ("Evento member_joined_channel", "@app.event(\"member_joined_channel\")"),
        ("Evento app_mention", "@app.event(\"app_mention\")"),
        ("Evento message", "@app.event(\"message\")"),
        ("Error handler", "@app.error"),
        ("Nombre Jarvis", "Jarvis"),
    ]
    
    all_found = True
    for name, element in required_elements:
        if element in content:
            print(f"  ✓ {name} encontrado")
        else:
            print(f"  ✗ {name} NO encontrado")
            all_found = False
    
    return all_found

def test_files_exist():
    """Verifica que todos los archivos necesarios existan"""
    print("\n✓ Probando existencia de archivos...")
    
    required_files = [
        "bot.py",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "README.md",
        "Procfile"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file} existe")
        else:
            print(f"  ✗ {file} NO existe")
            all_exist = False
    
    return all_exist

def test_requirements():
    """Verifica que requirements.txt tenga las dependencias necesarias"""
    print("\n✓ Probando requirements.txt...")
    
    try:
        with open("requirements.txt", 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("  ✗ requirements.txt no encontrado")
        return False
    
    required_deps = ["slack-bolt", "python-dotenv"]
    
    all_found = True
    for dep in required_deps:
        if dep in content:
            print(f"  ✓ {dep} encontrado en requirements.txt")
        else:
            print(f"  ✗ {dep} NO encontrado en requirements.txt")
            all_found = False
    
    return all_found

def test_env_example():
    """Verifica que .env.example tenga las variables necesarias"""
    print("\n✓ Probando .env.example...")
    
    try:
        with open(".env.example", 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("  ✗ .env.example no encontrado")
        return False
    
    required_vars = ["SLACK_BOT_TOKEN", "SLACK_SIGNING_SECRET", "SLACK_APP_TOKEN"]
    
    all_found = True
    for var in required_vars:
        if var in content:
            print(f"  ✓ {var} encontrado en .env.example")
        else:
            print(f"  ✗ {var} NO encontrado en .env.example")
            all_found = False
    
    return all_found

def main():
    """Ejecuta todas las pruebas"""
    print("="*60)
    print("PRUEBAS DEL BOT DE BIENVENIDA - JARVIS")
    print("="*60)
    
    tests = [
        test_files_exist,
        test_requirements,
        test_env_example,
        test_imports,
        test_bot_structure,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Error ejecutando {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Pruebas pasadas: {passed}/{total}")
    
    if all(results):
        print("\n✓ ¡TODAS LAS PRUEBAS PASARON!")
        return 0
    else:
        print("\n✗ Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main())

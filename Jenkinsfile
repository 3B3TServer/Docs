pipeline {
    agent any
    
    triggers {
        githubPush()
        pollSCM('H/5 * * * *')
    }
    
    environment {
        DOCS_BUILD_DIR = 'site'
        WEB_DIR = '/var/www/wiki'
    }
    
    stages {
        stage('🔄 Checkout') {
            steps {
                echo '📥 Загружаем код из GitHub...'
                checkout scm
                
                echo '📋 Информация о коммите:'
                sh '''
                    git log --oneline -1
                    echo "Ветка: $(git branch --show-current || echo 'detached')"
                '''
            }
        }
        
        stage('🔍 Проверка MkDocs') {
            steps {
                echo '🔍 Проверяем конфигурацию MkDocs...'
                sh '''
                    if [ -f "mkdocs.yml" ]; then
                        echo "✅ Найден mkdocs.yml"
                        mkdocs --version
                    else
                        echo "❌ mkdocs.yml не найден!"
                        exit 1
                    fi
                '''
            }
        }
        
        stage('🏗️ Сборка документации') {
            steps {
                echo '🏗️ Собираем документацию...'
                sh '''
                    rm -rf ${DOCS_BUILD_DIR}
                    mkdocs build --clean --verbose
                    
                    if [ -d "${DOCS_BUILD_DIR}" ] && [ "$(ls -A ${DOCS_BUILD_DIR})" ]; then
                        echo "✅ Сборка завершена успешно"
                        echo "📁 Содержимое директории сборки:"
                        ls -la ${DOCS_BUILD_DIR}/
                    else
                        echo "❌ Ошибка сборки"
                        exit 1
                    fi
                '''
            }
        }
        
        stage('🚀 Развертывание') {
            steps {
                echo '🚀 Развертываем на веб-сервер...'
                sh '''
                    if [ -d "${WEB_DIR}" ]; then
                        echo "💾 Создаем резервную копию..."
                        cp -r ${WEB_DIR} ${WEB_DIR}.backup.$(date +%Y%m%d_%H%M%S)
                        ls -dt ${WEB_DIR}.backup.* 2>/dev/null | tail -n +6 | xargs rm -rf 2>/dev/null || true
                    fi
                    
                    mkdir -p ${WEB_DIR}
                    echo "📋 Копируем файлы..."
                    cp -r ${DOCS_BUILD_DIR}/* ${WEB_DIR}/
                    chown -R www-data:www-data ${WEB_DIR} 2>/dev/null || true
                    chmod -R 755 ${WEB_DIR}
                    echo "✅ Развертывание завершено"
                '''
            }
        }
        
        stage('🧪 Проверка сайта') {
            steps {
                echo '🧪 Проверяем доступность сайта...'
                sh '''
                    if [ -f "${WEB_DIR}/index.html" ]; then
                        echo "✅ Главная страница найдена"
                        if curl -s -o /dev/null -w "%{http_code}" http://localhost/ | grep -q "200"; then
                            echo "✅ Сайт доступен"
                        else
                            echo "⚠️ Сайт может быть недоступен (проверьте настройки веб-сервера)"
                        fi
                    else
                        echo "❌ Главная страница не найдена"
                        exit 1
                    fi
                '''
            }
        }
    }
    
    post {
        success {
            echo '🎉 Документация успешно обновлена!'
            echo "🌐 Сайт: https://wiki.3b3t.fun/"
        }
        
        failure {
            echo '❌ Ошибка при обновлении документации'
            echo '📧 Проверьте логи Jenkins для диагностики'
        }
        
        always {
            echo '🧹 Очистка временных файлов...'
            sh 'rm -rf ${DOCS_BUILD_DIR} || true'
        }
    }
}

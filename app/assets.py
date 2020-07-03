from flask_assets import Bundle

base_css = ['css/standards.css', 'css/navbar.css']
home_css = ['css/home.css']
quizpage_base_css = ['css/quizpage-base.css']
quizpage_numeros_css = ['css/quizpage-numeros.css']
quizpage_mono_css = ['css/quizpage-mono.css']
quizpage_conjugacion_css = ['css/quizpage-conjugacion.css', 'css/checkbox-treeview.css']

base_js = ['js/navbar.js']
home_js = []
quizpage_base_js = ['js/enter.js', 'js/quizpage-common.js', 'js/errorReport.js']
quizpage_numeros_js = [
    'js/quizpage-numeros.js', 'js/texarea_cant_copy.js',
    'js/textarea_auto_height.js', 'js/textarea_disable_newline.js',
    'js/lib/recorder.js', 'js/audio_recording.js'
]
quizpage_mono_js = ['js/quizpage-mono.js']
quizpage_conjugacion_js = ['js/quizpage-conjugacion.js', 'js/checkbox-treeview.js']

bundles = {
    'base_css': Bundle(*base_css, filters='cssmin', output='dist/base.min.css'),
    'base_js': Bundle(*base_js, filters='jsmin', output='dist/base.min.js'),
    'home_css': Bundle(*base_css, *home_css, filters='cssmin',
                       output='dist/home.css'),
    'home_js': Bundle(*base_js, *home_js,
                      filters='jsmin', output='dist/home.min.js'),
    'quizpage_numeros_css': Bundle(*base_css, *quizpage_base_css, *quizpage_numeros_css,
                                   filters='cssmin', output='dist/quizpage_numeros.min.css'),
    'quizpage_numeros_js': Bundle(*base_js, *quizpage_base_js, *quizpage_numeros_js,
                                  filters='jsmin', output='dist/quizpage_numeros.min.js'),
    'qizpage_mono_css': Bundle(*base_css, *quizpage_base_css, *quizpage_mono_css,
                               filters='cssmin', output='dist/quizpage_mono.min.css'),
    'quizpage_mono_js': Bundle(*base_js, *quizpage_base_js, *quizpage_mono_js,
                               filters='jsmin', output='dist/quizpage_mono.min.js'),
    'quizpage_conjugacion_css': Bundle(*base_css, *quizpage_base_css, *quizpage_conjugacion_css,
                                       filters='cssmin', output='dist/quizpage_conjugacion.min.css'),
    'quizpage_conjugacion_js': Bundle(*base_js, *quizpage_base_js, *quizpage_conjugacion_js,
                                      filters='jsmin', output='dist/quizpage_conjugacion.min.js')
}

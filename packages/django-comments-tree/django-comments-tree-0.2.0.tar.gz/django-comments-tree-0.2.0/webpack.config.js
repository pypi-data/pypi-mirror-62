const path = require('path');
const webpack = require('webpack');

const STATIC_DIR = path.resolve(__dirname,
                                'django_comments_tree', 'static',
                                'django_comments_tree', 'js');
const SOURCE_DIR = path.resolve(STATIC_DIR, 'src');

module.exports = {
    mode: "none",
    devtool: 'source-map',
    entry: {
        plugin: path.resolve(SOURCE_DIR, 'index.js')
    },
    output: {
        filename: '[name]-1.4.0.js',
        path: STATIC_DIR
    },
    optimization: {
        splitChunks: {
            cacheGroups: {
                default: false,
                vendors: false,

                vendor: {
                    chunks: 'all',
                    test: /node_modules/
                }
            }
        }
    },
    module: {
        rules: [
            {
                test: /\.jsx?/,
                include: SOURCE_DIR,
                use: {
                    loader: 'babel-loader'
                }
            }
        ]
    },
    externals: {
        jquery: 'jQuery',
        bootstrap: 'bootstrap',
        django: 'django'
    }
};

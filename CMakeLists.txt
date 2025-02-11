cmake_minimum_required(VERSION 3.16)

project(Encryption VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 添加 SEAL 库的头文件路径（根据自己的文件路径更改）
include_directories(
    /home/SEAL/build/native/src
    /home/flutter/Work/Encryption
    /home/SEAL/build/thirdparty/msgsl-src/include
)

# 查找 Qt6 和 OpenCV
find_package(Qt6 REQUIRED COMPONENTS Core Concurrent Widgets)
find_package(OpenCV REQUIRED)

# 设置项目源文件
set(PROJECT_SOURCES
    main.cpp
    mainwindow.cpp
    mainwindow.h
    mainwindow.ui
)

# 创建 Qt 项目
if(QT_VERSION VERSION_GREATER_EQUAL "6")
    qt_add_executable(Encryption
        MANUAL_FINALIZATION
        ${PROJECT_SOURCES}
    )
else()
    add_executable(Encryption
        ${PROJECT_SOURCES}
    )
endif()

# 链接 Qt6 库
target_link_libraries(Encryption PRIVATE Qt6::Core Qt6::Concurrent Qt6::Widgets)

# 链接 SEAL 和 OpenCV 库
target_link_libraries(Encryption PRIVATE ${OpenCV_LIBS} -lseal-4.1)

# 设置目标包含路径（根据自己的文件路径更改）
target_include_directories(Encryption PRIVATE
    /home/SEAL/build/native/src
    /home/flutter/Work/Encryption
    /home/SEAL/build/thirdparty/msgsl-src/include
)

# SEAL 库路径（根据自己的文件路径更改）
link_directories(/home/SEAL/build/lib)

# 设置 CMake 安装路径
include(GNUInstallDirs)
install(TARGETS Encryption
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# 完成 Qt 可执行文件设置
if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(Encryption)
endif()

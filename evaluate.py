#!/usr/bin/python3

class Dependency():

    def __init__(self, line: str):
        words = line.split()
        self._package_name = words[0]
        # (>= foo) contains space, cannot use words easily

    @property
    def package_name(self):
        return self._package_name

    def print(self):
        print(f'Dependency: {self.package_name}')

class Package():

    def __init__(self, words, source_package: "SourcePackage"):
        self._name = words[0]
        self._type = words[1]
        self._section = words[2]
        self._priority = words[3]
        self._source_package = source_package

        if len(words) < 5:
            self._architectures = [source_package.architecture]
        else:
            self._architectures = self.parse_archs(words[4])
        self.check_type()
        self.check_priority()

    @property
    def source_package(self):
        return self._source_package

    @property
    def architectures(self):
        return self._architectures

    @property
    def name(self):
        return self._name

    def check_type(self):
        if self._type not in ['deb', 'udeb']:
            raise RuntimeError(f'unknown type {self._type}')

    def check_priority(self):
        if self._priority not in ['essential', 'required', 'important', 'standard', 'optional', 'extra']:
            raise RuntimeError(f'unknown priority {self._priority}')

    def parse_archs(self, line: str):
        if not line.startswith('arch='):
            raise RuntimeError(f'non an arch= string')
        line = line.split(sep='=')[1]
        return line.split(",")

    def print(self):
        arch_string = '|'.join(self._architectures)
        print(f'Package: {self._name} ({self._source_package.version}) [{arch_string}])')
        self._source_package.print()

class SourcePackage():

    def __init__(self, name: str):
        self.name = name
        self.packages = {}
        self._dependencies = {}

    def print(self):
        print(f'SourcePackage: {self.name} ({self._version}) [{self._architecture}]')
        for dependency in self._dependencies.values():
            dependency.print()

    @property
    def architecture(self):
        return self._architecture

    @architecture.setter
    def architecture(self, architecture: str):
        self._architecture = architecture

    @property
    def dependencies(self) -> dict[str, Dependency]:
        return self._dependencies

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version: str):
        self._version = version

    def add_dependency(self, dependency: Dependency):
        self._dependencies[dependency.package_name] = dependency

    def add_package(self, package: Package):
        self.packages[package._name] = package

class Evaluate():

    def parse_source(self, arch: str):
        file_name = f'./{arch}/Sources.txt'
        source_packages = {}
        packages = {}
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            source_package = None
            list = None
            for line in lines:
                if len(line) == 0:
                    continue
                words = line.split()
                if len(words) == 0:
                    continue
                if line[0] == ' ':
                    match list:
                        case 'Package-List:':
                            package = Package(words, source_package)
                            source_package.add_package(package)
                            packages[package.name] = package
                    continue
                list = None
                match words[0]:
                    case 'Architecture:':
                        source_package.architecture = words[1]
                    case 'Build-Depends:':
                        line = line[line.find(':') + 1:]
                        for dep_str in line.split(','):
                            dependency = Dependency(dep_str.strip())
                            source_package.add_dependency(dependency)
                    case 'Package:':
                        name = words[1]
                        source_package = SourcePackage(name)
                        source_packages[name] = source_package
                    case 'Package-List:':
                        list = 'Package-List:'
                    case 'Version:':
                        source_package.version = words[1]
        return packages, source_packages

    def parse_packages(self, arch: str):
        file_name = f'./{arch}/main/binary/Packages.txt'
        packages = set()
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            source_package = None
            list = None
            for line in lines:
                if len(line) == 0:
                    continue
                words = line.split()
                if len(words) == 0:
                    continue
                if line[0] == ' ':
                    continue
                match words[0]:
                    case 'Package:':
                        packages.add(words[1])
        return packages

    def __init__(self, ref_arch, arch):
        """constructor
        ref_arch -- reference architecture
        arch -- architecture to analyze
        """

        self.arch = arch
        self.ref_arch = ref_arch

        self.packages, self.source_packages = self.parse_source(ref_arch)
        self.ref_pkg_set = self.parse_packages(ref_arch)
        self.pkg_set = self.parse_packages(arch)

    def analyze_package(self, name: str):
        package: Package
        source_package: SourcePackage

        package = self.packages[name]
        print(f'{name} {package.architectures}')
        source_package = package.source_package
        for dependency in source_package.dependencies.values():
            if dependency.package_name in self.pkg_set:
                continue
            if dependency.package_name not in self.ref_pkg_set:
                continue
            print(f'missing dependency: {dependency.package_name}')


    def analyze(self):
        for name in self.ref_pkg_set:
            if name in self.pkg_set:
                continue
            self.analyze_package(name)

if __name__ == '__main__':
    ev = Evaluate('amd64', 'riscv64')
    ev.analyze()

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
        self._missing_rdepends = set[str]()
        self._missing = False

        if len(words) < 5:
            self._architectures = [source_package.architecture]
        else:
            self._architectures = self.parse_archs(words[4])
        self.check_type()
        self.check_priority()

    @property
    def source_package(self) -> "SourcePackage":
        return self._source_package

    @property
    def architectures(self) -> list[str]:
        return self._architectures

    @property
    def missing(self) -> bool:
        return self._missing

    @missing.setter
    def missing(self, value):
        self._missing = value

    @property
    def missing_rdepends(self):
        return self._missing_rdepends

    @property
    def name(self) -> str:
        return self._name

    def check_type(self) -> None:
        if self._type not in ['deb', 'udeb']:
            raise RuntimeError(f'unknown type {self._type}')

    def check_priority(self) -> None:
        if self._priority not in ['essential', 'required', 'important', 'standard', 'optional', 'extra']:
            raise RuntimeError(f'unknown priority {self._priority}')

    def parse_archs(self, line: str) -> list[str]:
        if not line.startswith('arch='):
            raise RuntimeError(f'non an arch= string')
        line = line.split(sep='=')[1]
        return line.split(",")

    def print(self):
        arch_string = '|'.join(self._architectures)
        print(f'Package: {self._name} ({self._source_package.version}) [{arch_string}])')
        self._source_package.print()

    def missing_rdepends_add(self, name: str):
        self._missing_rdepends.add(name)

class SourcePackage():

    def __init__(self, name: str):
        self._name = name
        self.packages = {}
        self._dependencies = {}

    def print(self):
        print(f'SourcePackage: {self._name} ({self._version}) [{self._architecture}]')
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
    def name(self) -> str:
        return self._name

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

    def parse_source_component(self, arch: str, component: str):
        source_packages: dict[str, SourcePackage] = {}
        packages: dict[str, Package] = {}
        file_name = f'./{arch}/{component}/Sources'

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

    def parse_source(self, arch: str, components: list[str]):
        source_packages: dict[str, SourcePackage] = {}
        packages: dict[str, Package] = {}

        for component in components:
            pkgs, src_pkgs = self.parse_source_component(arch, component)
            packages.update(pkgs)
            source_packages.update(src_pkgs)

        return packages, source_packages

    def parse_packages_component(self, arch: str, component: str):
        file_name = f'./{arch}/{component}/Packages'
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

    def parse_packages(self, arch: str, components: list[str]):
        packages = set()

        for component in components:
            packages.update(self.parse_packages_component(arch, component))
        return packages

    def __init__(self, ref_arch: str, arch: str, components: list[str]):
        """constructor
        ref_arch -- reference architecture
        arch -- architecture to analyze
        """

        self.arch = arch
        self.ref_arch = ref_arch

        self.packages, self.source_packages = self.parse_source(ref_arch, components)
        self.ref_pkg_set = self.parse_packages(ref_arch, components)
        self.pkg_set = self.parse_packages(arch, components)

        for name in self.ref_pkg_set:
            if name not in self.pkg_set and name in self.packages.keys():
                package = self.packages[name]
                package.missing = True

        pass

    def analyze_package(self, name: str, path: list[str]):
        package: Package
        source_package: SourcePackage

        if name in path:
            return
        if name not in self.packages.keys():
            return
        path.append(name)
        package = self.packages[name]
        depth = len(path)
        # print(f'{depth}: {name} {package.architectures} {package.source_package.name}')
        source_package = package.source_package
        for dependency in source_package.dependencies.values():
            if dependency.package_name in self.pkg_set:
                continue
            if dependency.package_name not in self.ref_pkg_set:
                continue
            # print(f'missing dependency: {dependency.package_name}')
            if dependency.package_name not in self.packages.keys():
                continue
            package = self.packages[dependency.package_name]
            package.missing_rdepends_add(name)
            self.analyze_package(dependency.package_name, path)
        path.remove(name)
        return

    def analyze(self):
        for name in self.ref_pkg_set:
            if name in self.pkg_set:
                continue
            self.analyze_package(name, [])

    def report(self):
        ranked_list : list[Package] = sorted(self.packages.values(), key=lambda package: -len(package.missing_rdepends))
        for package in ranked_list:
            count = len(package.missing_rdepends)
            if count > 0 or package.missing:
                print(f'#{count} {package.name} ({package.source_package.name})')
                if count > 0:
                    impacted =  ''.join([x + ',' for x in package.missing_rdepends])[:-1]
                    print(f'impacted: {impacted}')

if __name__ == '__main__':
    ev = Evaluate('amd64', 'riscv64', ['main','restricted','universe'])
    ev.analyze()
    ev.report()
    pass

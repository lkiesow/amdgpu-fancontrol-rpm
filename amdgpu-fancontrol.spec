%global commit 5461b365fb0810b4766a2d6328a8801d296c701f
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:      amdgpu-fancontrol
Summary:   Simple tool to control AMD graphics card fan
Version:   0
Release:   4.%{shortcommit}%{?dist}
License:   GPLv3
URL:       https://github.com/grmat/amdgpu-fancontrol
Source0:   https://github.com/grmat/amdgpu-fancontrol/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
BuildArch:      noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


%{?systemd_requires}
BuildRequires: systemd
Requires: bash


%description
Simple bash script to control AMD Radeon graphics cards fan pwm. Adjust
temp/pwm values and hysteresis/interval in the script as desired.


%prep
%autosetup -n amdgpu-fancontrol-%{commit}


%build
# deactivate debug mode
sed -i 's/^#DEBUG=true$/DEBUG=false/' etc-%{name}.cfg


%install
rm -rf $RPM_BUILD_ROOT

install -m 755 -d \
  %{buildroot}%{_bindir} \
  %{buildroot}%{_sysconfdir} \
  %{buildroot}%{_unitdir}
install -p -m 755 %{name} %{buildroot}%{_bindir}
install -p -m 644 etc-%{name}.cfg %{buildroot}%{_sysconfdir}/%{name}.cfg
install -p -m 644 %{name}.service %{buildroot}%{_unitdir}


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.md LICENSE
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name}.cfg

%changelog
* Fri Oct 18 2019 Lars Kiesow <lkiesow@uos.de> - 0-4
- Updated to 5461b36
- Deactivated debug mode

* Sat Oct 12 2019 Lars Kiesow <lkiesow@uos.de> - 0-3
- Updated to 78de47d

* Fri Nov 09 2018 Lars Kiesow <lkiesow@uos.de> - 0-2
- Updated to 3d62533

* Thu Nov 01 2018 Lars Kiesow <lkiesow@uos.de> - 0-1
- Initial build

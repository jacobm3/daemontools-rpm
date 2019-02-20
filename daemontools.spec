%define _name	daemontools
%define _ver	0.76
%define _dist	%(sh /usr/lib/rpm/redhat/dist.sh)
%define _rel	1%{?_dist}
%global debug_package %{nil}


Name:		%{_name}
Version:	%{_ver}
Release:	%{_rel}
Summary:	Service Monitoring and Logging Utilities
Group:		Unspecified
License:	Public Domain
URL:		http://cr.yp.to/daemontools.html
Source0:	http://cr.yp.to/daemontools/%{_name}-%{_ver}.tar.gz
Patch0:		daemontools-error.h.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root


%description
daemontools is a collection of tools for managing UNIX services.

supervise monitors a service. It starts the service and restarts the service
if it dies. Setting up a new service is easy: all supervise needs is a directory
with a run script that runs the service.

multilog saves error messages to one or more logs. It optionally timestamps each
line and, for each log, includes or excludes lines matching specified patterns.
It automatically rotates logs to limit the amount of disk space used.
If the disk fills up, it pauses and tries again, without losing any data.


%prep
%setup -q -n admin/%{_name}-%{_ver}
%patch0 -p0


%build
./package/compile


%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
cp -p command/* ${RPM_BUILD_ROOT}/usr/bin
cp -fp ${RPM_SOURCE_DIR}/svscanboot ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/etc/init
cp -p ${RPM_SOURCE_DIR}/daemontools.conf ${RPM_BUILD_ROOT}/etc/init



%clean
rm -rf ${RPM_BUILD_ROOT}


%post
[ -d /service ] || mkdir /service
initctl reload-configuration


%preun
initctl stop daemontools > /dev/null 2>&1 ||:


%postun
initctl reload-configuration

rmdir /service 2> /dev/null ||:


%files
%attr(0755,root,root) /usr/bin/envdir
%attr(0755,root,root) /usr/bin/envuidgid
%attr(0755,root,root) /usr/bin/fghack
%attr(0755,root,root) /usr/bin/multilog
%attr(0755,root,root) /usr/bin/pgrphack
%attr(0755,root,root) /usr/bin/readproctitle
%attr(0755,root,root) /usr/bin/setlock
%attr(0755,root,root) /usr/bin/setuidgid
%attr(0755,root,root) /usr/bin/softlimit
%attr(0755,root,root) /usr/bin/supervise
%attr(0755,root,root) /usr/bin/svc
%attr(0755,root,root) /usr/bin/svok
%attr(0755,root,root) /usr/bin/svscan
%attr(0555,root,root) /usr/bin/svscanboot
%attr(0755,root,root) /usr/bin/svstat
%attr(0755,root,root) /usr/bin/tai64n
%attr(0755,root,root) /usr/bin/tai64nlocal


%attr(0644,root,root) /etc/init/daemontools.conf



%changelog
* Tue Feb 19 2019 jacobm3 <jacobm3@gmail.com> 
- Simplified startup to attempt successful install in centos7 docker image
* Sun Jul 20 2014 teru <teru@kteru.net>
- Added startup script for el7
* Fri Sep 16 2011 teru <teru@kteru.net>
- Added startup script for el6
* Wed Mar 2 2011 teru <teru@kteru.net>
- Initial version


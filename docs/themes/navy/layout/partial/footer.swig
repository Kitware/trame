<footer id="footer" class="wrapper">
  <div class="inner">
    <div id="footer-copyright">
      &copy; {{ moment(Date.now()).year() }} <a href="{{ config.authorLink }}" target="_blank">{{ config.author }}</a>
    </div>

    <div id="footer-links">
      <a href="https://github.com/{{ config.github }}" class="footer-link" target="_blank"><i class="fa fa-github-alt"></i></a>
    </div>
  </div>
  <style>
    @media print {
      body { margin: 1.6cm; }
    
      aside {display: None;}
    
      footer {display: None;}
    
      nav {display: None;}
    
      div.print-break { page-break-before: always;}
    	
      h1 > a {display: None;}
      h2 > a {display: None;}
      h3 > a {display: None;}
      h4 > a {display: None;}
      h5 > a {display: None;}
      h6 > a {display: None;}

      a:empty {font-size: 0px;}
    }

  </style>
  <!--
    <a
      style="position: fixed; background: #00529b; color: white; top: 0; right: 0; height: 70px"
      href="https://www.kitware.com/careers"
    >
      <div style="position: relative; text-align: center;">
        <div
          style="margin-top: 5px; background: url(https://www.cmake.org/wp-content/uploads/2018/09/jobs_icon.png) no-repeat; background-size: 100%; width: 50px; height: 40px; margin: 5px auto 0;"
        ></div>
        <span style="padding: 5px 10px">Kitware is Hiring</span>
      </div>
    </a>
  -->
</footer>

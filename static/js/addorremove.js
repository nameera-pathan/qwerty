function addorremove(id) {
        if (id){
        var savejob= $('#jobsj'+id).data('sj');
        if(savejob == 0 ){
            $.ajax({
                url:"/users/save-job/" +id,
                method:"GET",
                success:function () {
                    $('#jobsj'+id).removeAttr("src");
                    $('#jobsj'+id).attr("src","https://cdn-icons-png.flaticon.com/512/2107/2107845.png");
                    const Toast = Swal.mixin({
                      toast: true,
                      position: 'top',
                      showConfirmButton: false,
                      timer: 2000,
                      timerProgressBar: false,
                      onOpen: (toast) => {
                        toast.addEventListener('mouseenter', Swal.stopTimer)
                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                      }
                    })

                    Toast.fire({
                      icon: 'success',
                      title: 'Job Saved Successfully!'
                    })
                    $('#jobsj'+id).data('sj',1);


                }

            });
            }else{

            $.ajax({
                url:"/users/remove-from-savedjobs/" +id,
                method:"GET",
                success:function () {
                    $('#jobsj'+id).removeAttr("src");
                    $('#jobsj'+id).attr("src","https://cdn-icons-png.flaticon.com/512/2107/2107952.png");
                  const Toast = Swal.mixin({
                      toast: true,
                      position: 'top',
                      showConfirmButton: false,
                      timer: 3000,
                      timerProgressBar: false,
                      onOpen: (toast) => {
                        toast.addEventListener('mouseenter', Swal.stopTimer)
                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                      }
                    })

                    Toast.fire({
                      icon: 'success',
                      title: 'Successfully removed from Saved Jobs'
                    })
                     $('#jobsj'+id).data('sj',0);

                }

            });

            }
        }
    }
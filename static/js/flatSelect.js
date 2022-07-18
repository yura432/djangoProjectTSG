$(function () {
      $('.tree li:has(ul)').addClass('parent_li').find(' > span').attr('title', 'Раскрыть эту ветку');
      $('.tree li.parent_li > span > i').on('click', function (e) {
          let children = $(this).parent().parent('li.parent_li').find(' > ul > li');
          if (children.is(":visible")) {
              children.hide('fast');
              $(this).parent().attr('title', 'Раскрыть эту ветку');
              $(this).html("+")
          } else {
              children.show('fast');
              $(this).parent().attr('title', 'Скрыть эту ветку');
              $(this).html("-")
          }
          e.stopPropagation();
      });
      $('.flat_cb').each(function (index, element) {
          if ($(element).is(':checked')) {
              checkState($(element).closest('span').addClass('full_select').closest('li.drop').find(' > span'), true)
          }

      }).on('click', function (e){
          if ($(this).is(':checked')) {
              $(this).parent().parent().find(' input ').prop('checked', true).closest(' span').addClass('full_select').removeClass('part_select')
          } else {
              $(this).parent().parent().find(' input ').prop('checked', false).closest(' span').removeClass('full_select').removeClass('part_select')
          }
          checkState($(this).closest('li.drop').find(' > span'), $(this).is(':checked'))
          e.stopPropagation();
      })
      $('.drop').find(' > span > input').on('click', function (e){
          if ($(this).is(':checked')) {
              $(this).parent().parent().find(' input ').prop('checked', true).closest(' span').addClass('full_select').removeClass('part_select')
          } else {
              $(this).parent().parent().find(' input ').prop('checked', false).closest(' span').removeClass('full_select').removeClass('part_select')
          }
          let thisLevelSpan = $(this).closest('li.drop').find(' > span')
          if (! thisLevelSpan.hasClass('top_drop')) {
              checkState($(this).closest('li.drop').parent().closest('li.drop').find(' > span'), $(this).is(':checked'))
          }
          e.stopPropagation();
      })
  });

function checkState(elem, check){
    if (!(elem.hasClass('full_select') || elem.hasClass('part_select')) && check){
        elem.addClass('part_select')
        if (!elem.hasClass('top_drop')) {
            checkState(elem.closest('li.drop').parent().closest('li.drop').find(' > span'), true)
        }
    } else if (elem.hasClass('full_select') && !check){
        elem.addClass('part_select').removeClass('full_select').find(' > input').prop('checked', false)
        if (!elem.hasClass('top_drop')) {
            checkState(elem.closest('li.drop').parent().closest('li.drop').find(' > span'), false)
        }
    } else if (elem.hasClass('part_select')){
        var full_select = true
        var no_select = true
        elem.parent().find('> ul ').children().each(function (index, element) {
            if (! $(element).find('> span').hasClass('full_select')){
                full_select = false
                return false
            }
        })
        if (full_select){
            elem.addClass('full_select').removeClass('part_select').find(' > input').prop('checked', true)
            if (!elem.hasClass('top_drop')) {
                checkState(elem.closest('li.drop').parent().closest('li.drop').find(' > span'), true)
            }
        }
        elem.parent().find('> ul ').children().each(function (index, element) {
            if ($(element).find('> span').hasClass('full_select') ||
            $(element).find('> span').hasClass('part_select')){
                no_select = false
                return false
            }
        })
        if (no_select){
            elem.removeClass('full_select').removeClass('part_select').find(' > input').prop('checked', false)
            if (!elem.hasClass('top_drop')) {
                checkState(elem.closest('li.drop').parent().closest('li.drop').find(' > span'), false)
            }
        }



    }
}
(define (problem blocks-5-0)
  (:domain blocks)
  (:objects
    a b c d e - block
  )
  (:init
    (clear d)
    (handempty)
    (on a b)
    (on c a)
    (on d e)
    (on e c)
    (ontable b)
  )
  (:goal (and
    (on b e)
    (on c b)
    (on d c)
    (on e a)
  ))
)

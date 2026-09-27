(define (problem blocks-5)
  (:domain blocks)
  (:objects
    a b c d e - block
  )
  (:init
    (on a b)
    (on c a)
    (on d e)
    (on e c)
    (ontable b)
    (clear d)
    (handempty)
  )
  (:goal (and
    (on b e)
    (on c b)
    (on d c)
    (on e a)
  ))
)
